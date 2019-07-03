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
import numpy as np


def reduce_to_binary(dataset, surviving_class, other_class=None):
    assert surviving_class in dataset.label_names

    if other_class is None:
        other_class = "!" + surviving_class

    index = np.where(dataset.label_names == surviving_class)[0][0]
    new_y = np.zeros((dataset.y.shape[0], 2))
    for i in range(0, dataset.y.shape[0]):
        if dataset.y[i, index]:
            new_y[i, 0] = 1
        else:
            new_y[i, 1] = 1
    dataset.y = new_y
    dataset.label_names = np.array([surviving_class, other_class])
    dataset.multilabel = False
