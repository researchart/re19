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
from __future__ import division

import logging
import random

import numpy as np
from sklearn.model_selection import KFold, ShuffleSplit, StratifiedShuffleSplit, StratifiedKFold


def train_test(model, dataset, test_size=0.1, stratify=False, seed=None, **kwargs):
    logging.getLogger(__name__).info("Performing a single train/test split. Test size: {}".format(test_size))

    if stratify and dataset.multilabel:
        logging.getLogger(__name__).warning("Stratify is not supported with multilabel classification")

    if stratify and not dataset.multilabel:
        splitter = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    else:
        splitter = ShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)

    for i_train, i_test in splitter.split(dataset.X, dataset.y):
        X_train, X_test, y_train, y_test = dataset.X[i_train], dataset.X[i_test], dataset.y[i_train], dataset.y[i_test]

    model.fit(X_train, y_train, **kwargs)

    p_train = model.predict(X_train)
    p_test = model.predict(X_test)

    return i_train, y_train, p_train, i_test, y_test, p_test


class PredefinedSplitsFolder(object):
    def __init__(self, fold_indices, shuffle=False):
        self.fold_indices = fold_indices
        self.fold_classes = set(fold_indices)
        self.shuffle = shuffle

    def split(self, X, y):
        for c in self.fold_classes:
            i_train = [index for (index, value) in enumerate(self.fold_indices) if value != c]
            i_test = [index for (index, value) in enumerate(self.fold_indices) if value == c]
            if self.shuffle:
                random.shuffle(i_train)
                random.shuffle(i_test)
            yield i_train, i_test


def cross_validation(model, dataset, n_splits=10, shuffle=True, seed=None, stratify=False, predefined_folds_file=None, **kwargs):
    assert not (stratify and predefined_folds_file)

    all_i_train = list()
    all_p_train = list()
    all_y_train = list()
    all_i_test = list()
    all_p_test = list()
    all_y_test = list()

    if predefined_folds_file and not stratify:
        with open(predefined_folds_file, 'r') as f:
            # This is a list of indices indicating fold membership of each input example. Comma separated. i.e. 5,1,1,8,3,0,...
            fold_indices = f.read()
        fold_indices = [int(i) for i in fold_indices.strip(',').split(',')]
        if len(fold_indices) != len(dataset.X):
            raise ValueError("Number of indices in predefined folds file does not match number of examples in dataset. Aborting.")
        folder = PredefinedSplitsFolder(fold_indices, shuffle=shuffle)
        n_splits = len(set(fold_indices))
        logging.getLogger(__name__).info("Performing predefined folds cross validation with {} folds.".format(n_splits))
    elif not predefined_folds_file and stratify:
        folder = StratifiedKFold(n_splits=n_splits, shuffle=shuffle, random_state=seed)
        logging.getLogger(__name__).info("Performing stratified cross validation with {} folds.".format(n_splits))
    elif not predefined_folds_file and not stratify:
        folder = KFold(n_splits=n_splits, shuffle=shuffle, random_state=seed)
        logging.getLogger(__name__).info("Performing cross validation with {} folds.".format(n_splits))

    fold_index = 1
    for i_train, i_test in folder.split(dataset.X, y=dataset.y):
        logging.getLogger(__name__).info("Training fold {} of {}".format(fold_index, n_splits))
        logging.getLogger(__name__).info("Training size: {}, Test size: {}".format(len(i_train), len(i_test)))

        X_train = dataset.X[i_train]
        X_test = dataset.X[i_test]
        y_train = dataset.y[i_train]
        y_test = dataset.y[i_test]

        logging.getLogger(__name__).info("Training set: " + str(np.sum(y_train, axis=0)))
        logging.getLogger(__name__).info("Test set    : " + str(np.sum(y_test, axis=0)))

        model.fit(X_train, y_train, **kwargs)

        p_train = model.predict(X_train)
        p_test = model.predict(X_test)

        all_i_train.extend(i_train)
        all_y_train.extend(y_train)
        all_p_train.extend(p_train)
        all_i_test.extend(i_test)
        all_y_test.extend(y_test)
        all_p_test.extend(p_test)

        fold_index += 1

    return np.asarray(all_i_train), np.asarray(all_y_train), np.asarray(all_p_train), np.asarray(all_i_test), np.asarray(all_y_test), np.asarray(all_p_test)



def train_only(model, dataset, **kwargs):
    model.fit(dataset.X, dataset.y, **kwargs)
    p_train = model.predict(dataset.X)
    return np.asarray(range(len(p_train))), dataset.y, p_train, None, None, None


def test_only(model, dataset, **kwargs):
    p_test = model.predict(dataset.X)
    return None, None, None, np.asarray(range(len(p_test))), dataset.y, p_test


def noop(model, dataset, **kwargs):
    return None, None, None, None, None, None
