#    Copyright (C) 2019  Jonas Winkler, Jannis Grönberg, Andreas Vogelsang
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import gzip
import json
import logging

import numpy as np
from keras import Sequential, Input, Model
from keras.callbacks import EarlyStopping
from keras.engine.saving import load_model
from keras.layers import Dense, Activation, Dropout, Embedding, Conv1D, concatenate

from custom_layers import custom_layers_dict, Select, OneMaxPooling1D
from utils import KerasConsoleLogger


class BaseModel(object):

    def __init__(self, dataset):
        self._dataset = dataset

    def prepare(self):
        pass

    def fit(self, x, y):
        pass

    def predict(self, x):
        pass

    def save(self, fn):
        logging.getLogger(__name__).warning("Model saving not implemented!")

    def export(self, fn, label_names):
        logging.getLogger(__name__).warning("Model export not implemented!")


class KerasModel(BaseModel):
    _model = None

    def __init__(self, dataset):
        super().__init__(dataset)

    def prepare(self, optimizer='adam'):
        loss = 'binary_crossentropy' if self._dataset.multilabel or self._dataset.binary else 'categorical_crossentropy'
        logging.getLogger(__name__).info("loss function: " + loss)
        self._model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
        logging.getLogger(__name__).info("Model summary:")
        self._model.summary(print_fn=logging.getLogger(__name__).info)
        self._w = self._model.get_weights()

    def fit(self, x, y, epochs=10, batch_size=16, early_stopping=True, early_stopping_patience=5, class_weighting=True, validation_split=0.):
        self._model.set_weights(self._w)
        callbacks = [KerasConsoleLogger()]

        if early_stopping:
            logging.getLogger(__name__).info("Early stopping is enabled.")
            callbacks.append(EarlyStopping(patience=early_stopping_patience, monitor='loss'))

        if class_weighting:
            class_weight = len(x) / np.sum(y, axis=0)
            logging.getLogger(__name__).info("Using class weights in training: " + str(class_weight))
        else:
            class_weight = None
            logging.getLogger(__name__).info("Not using class weights in training.")

        logging.getLogger(__name__).info("Starting training.")
        self._model.fit(x, y, batch_size=batch_size, epochs=epochs, callbacks=callbacks, class_weight=class_weight, verbose=0, validation_split=validation_split)
        logging.getLogger(__name__).info("Training finished.")

    def predict(self, x):
        return self._model.predict(x)

    def save(self, fn):
        self._model.save(fn)


class SavedKerasModel(KerasModel):

    def __init__(self, dataset, model_file):
        super().__init__(dataset)
        self._model = load_model(model_file, custom_objects=custom_layers_dict)
        assert (None,) + dataset.get_input_shape() == self._model.input_shape
        assert (None,) + dataset.get_output_shape() == self._model.output_shape


class ZeroRModel(BaseModel):

    def __init__(self, dataset):
        BaseModel.__init__(self, dataset)

    def prepare(self):
        pass

    def fit(self, x, y):
        if self._dataset.multilabel:
            self._label = np.sum(y, axis=0) / len(y)
        else:
            self._label = np.unique(y, axis=0)[0]
        logging.getLogger(__name__).info("ZeroR using {} as label for prediction".format(self._label))

    def predict(self, x):
        return np.asarray([self._label for e in x])


class WordCNNModel(KerasModel):

    def __init__(self, dataset, filter_sizes, num_filters_per_size, layers=[], conv_activation='linear', layer_activation='relu', trainable_embeddings=False):
        super().__init__(dataset)

        assert len(filter_sizes) > 0
        assert num_filters_per_size > 0
        assert len(dataset.get_input_shape()) == 1
        assert len(dataset.get_output_shape()) == 1

        self._dataset = dataset
        self._filter_sizes = filter_sizes
        self._num_filters_per_size = num_filters_per_size
        self._conv_activation = conv_activation
        self._layer_activation = layer_activation

        inputs = Input(shape=dataset.get_input_shape())
        self._emb_layer = Embedding(input_dim=dataset.word_embedding_model.get_vocab_size(), output_dim=dataset.word_embedding_model.get_embeddings_size(), weights=[dataset.word_embedding_model.get_embeddings()], trainable=trainable_embeddings)
        emb = self._emb_layer(inputs)

        filters = []
        self._conv = {}
        for filter_size in filter_sizes:
            layer = Conv1D(num_filters_per_size, filter_size, padding='valid', activation=conv_activation)
            self._conv[filter_size] = layer
            layer = OneMaxPooling1D(axis=1, keepdims=False)(layer(emb))
            filters.append(layer)

        if len(filters) >= 2:
            result = concatenate(filters, axis=1)
        else:
            result = filters[0]

        self._layers = list()

        for l in layers:
            layer = Dense(l, activation=layer_activation)
            self._layers.append(layer)
            result = layer(result)

        self._output_layer = Dense(dataset.get_output_shape()[0], activation='sigmoid' if dataset.multilabel or dataset.binary else 'softmax')
        output = self._output_layer(result)

        self._model = Model(inputs=inputs, outputs=output)

    def export(self, fn, label_names):
        with gzip.GzipFile(fn, "w") as f:
            json_str = json.dumps({
                'w2v': {
                    'vocab': self._dataset.word_embedding_model.get_vocab(),
                    'emb': self._emb_layer.get_weights()[0].tolist(),
                    'sentence_length': self._dataset.X.shape[1]
                },
                'label_names': self._dataset.label_names.tolist(),
                'layers': [{'W': l.get_weights()[0].tolist(), 'b': l.get_weights()[1].tolist()} for l in self._layers],
                'filters_W': {filter_size: f.get_weights()[0].tolist() for (filter_size, f) in self._conv.items()},
                'filters_b': {filter_size: f.get_weights()[1].tolist() for (filter_size, f) in self._conv.items()},

                'filter_sizes': self._filter_sizes,
                'num_filters_per_size': self._num_filters_per_size,
                'conv_activation': self._conv_activation,
                'layer_activation': self._layer_activation,

                'output_layer': {'W': self._output_layer.get_weights()[0].tolist(),
                                 'b': self._output_layer.get_weights()[1].tolist()},
            }, indent=2)
            f.write(json_str.encode('utf-8'))
