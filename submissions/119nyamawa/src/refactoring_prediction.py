import nltk
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

# classifiers = ['SVM', 'NB', 'MNB', 'BNB', 'LR', 'RF']
classifiers = ['LR']
# data loading
featuresets_f = open("./feature_modeling/testing_featureset.pickle", "rb")
testing_set = pickle.load(featuresets_f)
featuresets_f.close()
print("lenght of testing dataset: ", len(testing_set))

for t_index in range(10):

    print("iteration " + str(t_index + 1))
    featuresets_f = open("./feature_modeling/training_featureset" + str(t_index + 1) + ".pickle", "rb")
    training = pickle.load(featuresets_f)
    featuresets_f.close()
    print("lenght of training dataset: ", len(training))

    for cls in classifiers:
        if cls == 'SVM':
            classifier = SklearnClassifier(LinearSVC())
            classifier.train(training)
        elif cls == 'NB':
            classifier = nltk.NaiveBayesClassifier.train(training)
            classifier.train(training)
        elif cls == 'MNB':
            classifier = SklearnClassifier(MultinomialNB())
            classifier.train(training)
        elif cls == 'BNB':
            classifier = SklearnClassifier(BernoulliNB())
            classifier.train(training)
        elif cls == 'LR':
            classifier = SklearnClassifier(LogisticRegression())
            classifier.train(training)
        elif cls == 'RF':
            classifier = SklearnClassifier(RandomForestClassifier())
            classifier.train(training)
        # prediction
        y_true, y_pred = [], []

        for i, (feats, label_true) in enumerate(testing_set):
            label_pred = classifier.classify(feats)
            y_true.append(label_true)
            y_pred.append(label_pred)

        # save_classifier = open("./trained_classifiers/LRall.pickle", "wb")
        save_classifier = open("./trained_classifiers/" + cls + str(t_index + 1) + ".pickle", "wb")
        pickle.dump(classifier, save_classifier)
        save_classifier.close()

        # save_classifier = open("./y_true_pred/y_true_LRall.pickle", "wb")
        save_classifier = open("./y_true_pred/y_true_" + cls + str(t_index + 1) +  ".pickle", "wb")
        pickle.dump(y_true, save_classifier)
        save_classifier.close()

        # save_classifier = open("./y_true_pred/y_pred_LRall.pickle", "wb")
        save_classifier = open("./y_true_pred/y_pred_" + cls + str(t_index + 1) +  ".pickle", "wb")
        pickle.dump(y_pred, save_classifier)
        save_classifier.close()

        print(cls + " for iteration " + str(t_index + 1) + " done.....")
        print("=========>>")