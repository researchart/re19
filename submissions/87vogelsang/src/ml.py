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
import os

os.environ["MKL_THREADING_LAYER"] = "GNU"
import drivers
from models import *
import postprocessing
import preprocessing
from readers import *
from utils import MyJsonEncoder

import json
import logging
import sys
from datetime import datetime

from keras.optimizers import SGD, Adam, Adagrad, RMSprop

from report import build_report

optimizers = {'sgd': SGD,
              'adam': Adam,
              'adagrad': Adagrad,
              'rmsprop': RMSprop}

models = {'saved_keras_model': SavedKerasModel,
          'word_cnn': WordCNNModel,
          'zeror': ZeroRModel}

readers = {'word_emb': word_embedding_sentence_reader}

training_drivers = {'train_test': drivers.train_test,
                    'cv': drivers.cross_validation,
                    'test_only': drivers.test_only,
                    'train_only': drivers.train_only,
                    'noop': drivers.noop}

preprocessing_functions = {'reduce_to_binary': preprocessing.reduce_to_binary}

postprocessing_functions = {'label_dependencies': postprocessing.label_dependencies}


def cfg_get(cfg, key, default=None, required=True):
    if key in cfg:
        return cfg[key]
    elif default is not None:
        return default
    elif required:
        raise ValueError("config option " + key + " is missing.")
    else:
        return None


def run_experiment(cfg):
    logging.getLogger(__name__).info("Initializing reader " + cfg_get(cfg, 'reader'))
    reader = readers[cfg_get(cfg, 'reader')]

    logging.getLogger(__name__).info("Reading dataset...")
    dataset = reader(cfg_get(cfg, 'input'), **cfg_get(cfg, 'reader_params', {}))

    preprocessing_steps = cfg_get(cfg, 'preprocessing', [])
    for step in preprocessing_steps:
        step_name = step['name']
        step_params = step['params'] if 'params' in step else {}
        logging.getLogger(__name__).info("Running pre processing step " + step_name)
        preprocessing_functions[step_name](dataset=dataset, **step_params)

    logging.getLogger(__name__).info("Initializing model " + cfg_get(cfg, 'model'))
    model = models[cfg_get(cfg, 'model')](dataset=dataset, **cfg_get(cfg, 'model_params', {}))

    if cfg_get(cfg, 'optimizer', required=False) is not None:
        logging.getLogger(__name__).info("Initializing optimizer " + str(cfg_get(cfg, 'optimizer', required=False)))
        optimizer = optimizers[cfg_get(cfg, 'optimizer', required=False)](**cfg_get(cfg, 'optimizer_params', {}))
    else:
        optimizer = None

    logging.getLogger(__name__).info("Preparing the model...")
    if optimizer is not None:
        model.prepare(optimizer=optimizer)
    else:
        model.prepare()

    logging.getLogger(__name__).info("Inizializing driver " + cfg_get(cfg, 'driver', 'train_test'))
    driver = training_drivers[cfg_get(cfg, 'driver', 'train_test')]

    logging.getLogger(__name__).info("Calling driver...")
    t_start = datetime.now()
    i_train, y_train, p_train, i_test, y_test, p_test = driver(model, dataset, **cfg_get(cfg, 'driver_params', {}))
    t_end = datetime.now()

    report = build_report(y_train, p_train, y_test, p_test, dataset, (t_end - t_start).total_seconds())

    report['config'] = cfg

    postprocessing_steps = cfg_get(cfg, 'postprocessing', [])

    report['postprocessing'] = {}

    for step in postprocessing_steps:
        step_name = step['name']
        step_params = step['params'] if 'params' in step else {}
        logging.getLogger(__name__).info("Running postprocessing step " + step_name)
        report['postprocessing'][step_name] = postprocessing_functions[step_name](dataset=dataset, report=report, i_train=i_train, y_train=y_train, p_train=p_train, i_test=i_test, y_test=y_test, p_test=p_test, **step_params)

    if 'model_save_file' in cfg:
        logging.getLogger(__name__).info("Saving model to file " + cfg['model_save_file'])
        model.save(cfg['model_save_file'])

    if 'model_export_file' in cfg:
        logging.getLogger(__name__).info("Exporting model to file " + cfg['model_export_file'])
        model.export(cfg['model_export_file'], dataset.label_names)

    return report


def run_experiment_from_file(config_file):
    logging.getLogger(__name__).info("Reading configuration file " + config_file)
    with open(config_file, 'r') as f:
        cfg = json.load(f)

    return run_experiment(cfg)


class ArrayHandler(logging.Handler):
    messages = []

    def emit(self, record):
        self.messages.append(self.format(record))


if __name__ == '__main__':
    handler = ArrayHandler()
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(), handler])
    if len(sys.argv) < 2:
        cfg_file = '../conf/reqinf-de-wcnn.json'
    else:
        cfg_file = sys.argv[1]
    report = run_experiment_from_file(cfg_file)

    report_file = "../reports/" + os.path.splitext(os.path.basename(cfg_file))[0] + "-" + datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S") + "-report.json"
    logging.getLogger(__name__).info("Writing report to file " + report_file)
    with open(report_file, 'w') as f:
        report['log'] = handler.messages
        json.dump(report, f, indent=2, cls=MyJsonEncoder, sort_keys=True)
