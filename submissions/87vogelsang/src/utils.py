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
import datetime
import json
import logging
import numpy as np
import time

from keras.callbacks import Callback


class KerasConsoleLogger(Callback):

    def __init__(self):
        super().__init__()

    def on_train_begin(self, logs=None):
        self.epochs = self.params['epochs']

    def on_epoch_begin(self, epoch, logs=None):
        self.seen = 0
        self.log_values = []
        self.epoch_start = time.time()

    def on_epoch_end(self, epoch, logs=None):
        epoch_end = time.time()
        logs = logs or {}
        message = "Epoch {} of {} done.".format(epoch + 1, self.epochs)
        message += " {}: {:.2f}s".format("time", epoch_end - self.epoch_start)
        for k in sorted(logs.keys()):
            message += " {}: {}".format(k, logs[k])
        logging.getLogger(__name__).info(message)


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        else:
            return super(MyJsonEncoder, self).default(obj)


def make_id_dict(l):
    d = {}
    for idx, e in enumerate(l):
        d[e] = idx
    return d


def pad(l, length, pad_element=0):
    return l[0:length] if len(l) >= length else l + ([pad_element] * (length - len(l)))


def flatten(l):
    return [item for sublist in l for item in sublist]
