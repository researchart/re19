All the source code files are in src directory and they can be run in the order they appear in the directory. Note that, these are python files and therefore you would need python environment to run the files.

Further note that, you would need to redefine the directory path from which the training and testing dataset is populated.

If the source code run successful, the results will appear on the console.  

_TIMM HERE: : ehre is a list of the imports. looks like this needs pandas, nltk, scikitlearn. i'd install those before doing anything else'_

```
create_dataset.py:import pandas as pd
create_dataset.py:import pickle
feature_words.py:import pickle
feature_words.py:from nltk import word_tokenize, pos_tag
feature_words.py:from nltk.stem import WordNetLemmatizer
feature_words.py:import re
feature_words.py:from collections import Counter
feature_words.py:import string
feature_words.py:import numpy as np
feature_words.py:import math
featuresets_generation.py:import pickle
featuresets_generation.py:import random
multi-label_classifiers.py:import pandas as pd
multi-label_classifiers.py:from sklearn.feature_extraction.text import CountVectorizer
multi-label_classifiers.py:from sklearn.feature_extraction.text import TfidfTransformer
multi-label_classifiers.py:from sklearn.preprocessing import MultiLabelBinarizer
multi-label_classifiers.py:from sklearn.model_selection import train_test_split
multi-label_classifiers.py:from imblearn.over_sampling import RandomOverSampler
multi-label_classifiers.py:from sklearn.naive_bayes import MultinomialNB
multi-label_classifiers.py:from sklearn.svm import LinearSVC
multi-label_classifiers.py:from sklearn.linear_model import LogisticRegression
multi-label_classifiers.py:from sklearn.multiclass import OneVsRestClassifier
multi-label_classifiers.py:from sklearn.metrics import hamming_loss, accuracy_score, precision_score, recall_score, f1_score, classification_report
multi-label_classifiers.py:import numpy as np
multi-label_classifiers.py:import seaborn as sns
multi-label_classifiers.py:import matplotlib.pyplot as plt
multi-label_classifiers.py:import pyodbc
multi-label_classifiers.py:from nltk.stem import PorterStemmer
multi-label_classifiers.py:from nltk.corpus import stopwords
multi-label_classifiers.py:import re
refactoring_prediction.py:import nltk
refactoring_prediction.py:from nltk.classify.scikitlearn import SklearnClassifier
refactoring_prediction.py:import pickle
refactoring_prediction.py:from sklearn.naive_bayes import MultinomialNB, BernoulliNB
refactoring_prediction.py:from sklearn.linear_model import LogisticRegression
refactoring_prediction.py:from sklearn.ensemble import RandomForestClassifier
refactoring_prediction.py:from sklearn.svm import LinearSVC
```
			
