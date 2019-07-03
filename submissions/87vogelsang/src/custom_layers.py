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
from keras import backend as K
from keras.engine.topology import Layer
from theano.tensor.signal import pool

import theano.tensor as T


class OneMaxPooling1D(Layer):
    def __init__(self, axis=1, keepdims=False, **kwargs):
        super(OneMaxPooling1D, self).__init__(**kwargs)
        self._axis = axis
        self._keepdims = keepdims

    def call(self, x, mask=None):
        return K.max(x, self._axis, keepdims=self._keepdims)

    def compute_output_shape(self, input_shape):
        if self._keepdims:
            return tuple(x if i != self._axis else 1 for (i, x) in enumerate(input_shape))
        else:
            return tuple(x for (i, x) in enumerate(input_shape) if i != self._axis)


class Select(Layer):
    def __init__(self, axis, index, **kwargs):
        super(Select, self).__init__(**kwargs)
        self._axis = axis
        self._index = index

    def build(self, input_shape):
        self._input_rank = len(input_shape)
        Layer.build(self, input_shape)

    def call(self, x, mask=None):
        slc = [slice(None)] * self._input_rank
        slc[self._axis] = self._index
        return x[slc]

    def compute_output_shape(self, input_shape):
        return tuple(x for (i, x) in enumerate(input_shape) if i != self._axis)


class KMaxPooling1D(Layer):
    def __init__(self, axis, k, **kwargs):
        self.axis = axis
        self.k = k
        super(KMaxPooling1D, self).__init__(**kwargs)

    def build(self, input_shape):
        assert len(input_shape) > self.axis >= 0
        self.input_rank = len(input_shape)
        Layer.build(self, input_shape)

    def call(self, x, mask=None):
        idx = []
        for i in range(self.input_rank):
            if i == self.axis:
                idx2 = [slice(-self.k, None) if i2 == self.axis else slice(None) for i2 in range(self.input_rank)]
                idx.append(T.sort(T.argsort(x, axis=self.axis)[tuple(idx2)], axis=self.axis))
            else:
                idx.append(T.arange(x.shape[i]).dimshuffle(*[0 if i2 == i else "x" for i2 in range(self.input_rank)]))
        return x[tuple(idx)]

    def compute_output_shape(self, input_shape):
        return tuple([self.k if i == self.axis else input_shape[i] for i in range(len(input_shape))])


class Folding(Layer):
    def __init__(self, k, **kwargs):
        self.k = k
        super(Folding, self).__init__(**kwargs)

    def call(self, x, mask=None):
        return pool.pool_2d(x, ds=(1, self.k), mode='sum', ignore_border=True)

    def compute_output_shape(self, input_shape):
        return tuple(
            [input_shape[i] / self.k if i == len(input_shape) - 1 else input_shape[i] for i in range(len(input_shape))])


custom_layers_dict = {"OneMaxPooling1D": OneMaxPooling1D, "SelectLayer": Select, "KMaxPooling1D": KMaxPooling1D,
                      "Folding": Folding}
