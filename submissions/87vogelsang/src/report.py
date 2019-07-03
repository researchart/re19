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
import logging
import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, roc_auc_score, coverage_error, \
    label_ranking_loss, precision_recall_curve, roc_curve
from sklearn.metrics.classification import accuracy_score


def build_report(y_train, p_train, y_test, p_test, dataset, execution_time):
    report = {}

    if dataset.multilabel:
        metrics = build_multilabel_metrics(y_train, p_train, y_test, p_test, dataset)
    else:
        metrics = build_metrics(y_train, p_train, y_test, p_test, dataset)

    report['metrics'] = metrics
    report['execution_time'] = execution_time
    report['date_created'] = datetime.datetime.now()

    return report


def build_multilabel_metrics(y_train, p_train, y_test, p_test, dataset):
    metrics = {}

    if y_train is not None and p_train is not None:
        # nothing to do here
        pass
    else:
        logging.getLogger(__name__).warning("No training data available during report generation.")

    if y_test is not None and p_test is not None:
        p_test_round = np.array(p_test.round(), dtype=np.int64)
        metrics['label_ranking_loss'] = label_ranking_loss(y_test, p_test_round)
        metrics['coverage_error'] = coverage_error(y_test, p_test_round)

        metrics['hamming_loss'] = np.sum(np.not_equal(y_test, p_test_round)) / float(y_test.size)
        metrics['exact_match'] = np.sum([np.sum(row) == 0 for row in np.not_equal(y_test, p_test_round)]) / len(y_test)
        metrics['accuracy'] = np.sum([np.sum(t * p) / np.sum(t | p) for [t, p] in np.stack((y_test, p_test_round), axis=1)]) / len(y_test)

        metrics['classes'] = []

        p, r, f1, s = precision_recall_fscore_support(y_test, p_test_round, average=None, warn_for=[])
        for (i, l) in enumerate(dataset.label_names):
            metrics['classes'].append({
                'name': l,
                'recall': r[i],
                'precision': p[i],
                'f1': f1[i],
                'support': s[i]})

        metrics['curves'] = []
        for (i, l) in enumerate(dataset.label_names):
            metrics['curves'].append({
                'name': l,
                'precision_recall_curve': precision_recall_curve(y_test[:, i], p_test[:, i]),
                'roc_curve': roc_curve(y_test[:, i], p_test[:, i])
            })

        metrics['samples_average_precision'], metrics['samples_average_recall'], metrics['samples_average_f1'], _ = precision_recall_fscore_support(y_test, p_test_round, average='samples', warn_for=[])
        metrics['micro_average_precision'], metrics['micro_average_recall'], metrics['micro_average_f1'], _ = precision_recall_fscore_support(y_test, p_test_round, average='micro', warn_for=[])
        metrics['macro_average_precision'], metrics['macro_average_recall'], metrics['macro_average_f1'], _ = precision_recall_fscore_support(y_test, p_test_round, average='macro', warn_for=[])
    else:
        logging.getLogger(__name__).warning("No test data available during report generation.")

    return metrics


def build_metrics(y_train, p_train, y_test, p_test, dataset):
    metrics = {}

    if y_train is not None and p_train is not None:
        y_train_argmax = y_train if dataset.binary else np.argmax(y_train, axis=1)
        p_train_argmax = p_train.round() if dataset.binary else np.argmax(p_train, axis=1)
        metrics['final_train_accuracy'] = accuracy_score(p_train_argmax, y_train_argmax)
    else:
        logging.getLogger(__name__).warning("No training data available during report generation.")

    if y_test is not None and p_test is not None:
        y_test_argmax = y_test if dataset.binary else np.argmax(y_test, axis=1)
        p_test_argmax = p_test.round() if dataset.binary else np.argmax(p_test, axis=1)

        metrics['accuracy'] = accuracy_score(y_test_argmax, p_test_argmax)
        metrics['confusion_matrix'] = confusion_matrix(y_test_argmax, p_test_argmax)

        metrics['classes'] = []
        p, r, f1, s = precision_recall_fscore_support(y_test_argmax, p_test_argmax, average=None)
        for (i, l) in enumerate(dataset.label_names):
            metrics['classes'].append({
                'name': l,
                'recall': r[i],
                'precision': p[i],
                'f1': f1[i],
                'support': s[i]
            })

        if dataset.binary:
            metrics['precision_recall_curve'] = precision_recall_curve(y_test, p_test)
            metrics['roc_curve'] = roc_curve(y_test, p_test)
        else:
            metrics['curves'] = []
            for (i, l) in enumerate(dataset.label_names):
                metrics['curves'].append({
                    'name': l,
                    'precision_recall_curve': precision_recall_curve(y_test[:, i], p_test[:, i]),
                    'roc_curve': roc_curve(y_test[:, i], p_test[:, i])
                })

    else:
        logging.getLogger(__name__).warning("No test data available during report generation.")

    return metrics
