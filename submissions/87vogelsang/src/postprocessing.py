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

import numpy as np


def label_dependencies(dataset, **kwargs):
    if not dataset.multilabel:
        logging.getLogger(__name__).error("Label dependencies can only be determined in a multilabel dataset!")
        return {}

    num_classes = dataset.y.shape[1]
    dependency_matrix_if = np.zeros(shape=(num_classes, num_classes))
    dependency_matrix_then = np.zeros(shape=(num_classes, num_classes))
    for label in dataset.y:
        for class_if in np.arange(num_classes):
            for class_then in np.arange(num_classes):
                if label[class_if]:
                    dependency_matrix_if[class_if][class_then] += 1
                    if label[class_then]:
                        dependency_matrix_then[class_if][class_then] += 1

    dependency_matrix = dependency_matrix_then / dependency_matrix_if

    return dependency_matrix
