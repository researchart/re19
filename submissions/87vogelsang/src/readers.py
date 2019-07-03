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
import logging
import os
import collections

import keras
import numpy as np

from emb_models import PretrainedGenSimWordEmbeddingModel, GenSimWordEmbeddingModel
from utils import make_id_dict, pad, flatten


class DataSet(object):
    multilabel = False
    is_binary = False

    def __len__(self):
        return self.X.shape[0]

    def __init__(self, X, y, label_names, X_raw):
        self.X = X
        self.y = y
        self.label_names = label_names
        self.X_raw = X_raw

    def get_input_shape(self):
        return self.X.shape[1:]

    def get_output_shape(self):
        return self.y.shape[1:]


class WordEmbeddingDataSet(DataSet):
    def __init__(self, X, y, label_names, word_embedding_model, X_raw=None):
        super().__init__(X, y, label_names, X_raw)
        self.word_embedding_model = word_embedding_model


def make_binary_label_vectors(labels):
    id2label = sorted(list(set(labels)))
    assert len(id2label) == 2
    return np.array([ [id2label.index(l)] for l in labels]), np.array(id2label)


def make_onehot_label_vectors(labels):
    id2label = sorted(list(set(labels)))
    label2id = make_id_dict(id2label)
    label_ids = [label2id[l] for l in labels]
    return keras.utils.to_categorical(label_ids), np.array(id2label)


def _make_multilabel_label_vector(classes, id2label):
    return [1 if id2label[i] in classes else 0 for i in range(len(id2label))]


def make_multilabel_label_vectors(labels, label_separator):
    labels_splitted = [l.split(label_separator) if len(l) > 0 else [] for l in labels]
    id2label = list(set([label.strip() for sublist in labels_splitted for label in sublist]))
    result = [_make_multilabel_label_vector(l, id2label) for l in labels_splitted]
    return np.asarray(result), np.array(id2label)


def make_label_vectors(labels, multilabel, binary, label_separator):
    if multilabel:
        return make_multilabel_label_vectors(labels, label_separator) + (False,)
    elif binary == True or (binary == 'auto' and len(set(labels)) == 2):
        return make_binary_label_vectors(labels) + (True,)
    else:
        return make_onehot_label_vectors(labels) + (False,)


def read_simple_dataset_files(source_files, encoding, separator):
    assert source_files is not None
    assert len(source_files) > 0
    assert all(os.path.exists(f) for f in source_files)

    sentences = []
    labels = []
    for source_file in source_files:
        with open(source_file, 'r', encoding=encoding) as f:
            for s in f.readlines():
                sentences.append(s.strip()[s.index(separator) + 1:])
                labels.append(s.strip()[0:s.index(separator)])
    return sentences, labels


def word_embedding_sentence_reader(source_files, model_file=None, model_conf=None, sentence_length=None, multilabel=False, binary='auto', separator=" ", label_separator=",", encoding='utf-8', override_labels=None):

    sentences, labels = read_simple_dataset_files(source_files, encoding, separator)

    if model_file is not None:
        assert os.path.isfile(model_file)
        model = PretrainedGenSimWordEmbeddingModel(model_file)
    elif model_conf is not None:
        model = GenSimWordEmbeddingModel(**model_conf)
    else:
        raise ValueError("No embedding model specified.")
    sentence_ids = [[model.get_vocab()[w] if w in model.get_vocab() else -1 for w in sentence.split(' ')] for sentence in sentences]

    print(sentence_ids)

    c = collections.Counter(flatten(sentence_ids))
    logging.getLogger(__name__).info("Word Embedding statistics: {} total words, {} unknown words, {} fraction of known words".format(sum(c.values()), c[-1], 1 - c[-1] / sum(c.values())))

    if sentence_length is not None:
        logging.getLogger(__name__).info("Average sentences length: {}".format(np.average([len(sentence) for sentence in sentence_ids])))
        dropped_words = sum([max(0, len(sentence) - sentence_length) for sentence in sentence_ids])
        oversized_examples = sum([1 if len(sentence) > sentence_length else 0 for sentence in sentence_ids])
        logging.getLogger(__name__).info("{} examples are too long. Going to drop {} words ({} percent)".format(oversized_examples, dropped_words, dropped_words / sum(c.values()) * 100))
        sentence_ids = [pad(sentence, sentence_length, -1) for sentence in sentence_ids]

    label_vector, label_names, is_binary = make_label_vectors(labels, multilabel, binary, label_separator)

    if override_labels:
        if len(override_labels) == len(label_names):
            label_names = np.asarray(override_labels)
        else:
            logging.getLogger(__name__).warning('Cannot override labels: number of labels does not match!')

    logging.getLogger(__name__).info("Dataset read. {} examples, {} classes ({}), w2v vocab size: {}, w2v emb size: {}, multilabel: {}".format(len(sentences), len(label_names), label_names, model.get_vocab_size(), model.get_embeddings_size(), "yes" if multilabel else "no"))

    dataset = WordEmbeddingDataSet(np.asarray(sentence_ids), label_vector, label_names, model, np.array(sentences))
    dataset.multilabel = multilabel
    dataset.binary = is_binary
    return dataset
