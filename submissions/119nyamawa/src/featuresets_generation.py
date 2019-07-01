import pickle
import random

def load_dataset():
    file = open("./dataset/shuffle_dataset.pickle", "rb")
    dataset = pickle.load(file)
    file.close()
    print("dataset of length " , len(dataset) , " is loaded.....")
    return dataset

def load_features():
    # file = open("./dataset/features.pickle", "rb")
    file = open("./dataset/features_without_pp.pickle", "rb")
    features = pickle.load(file)
    file.close()
    print("features of length " , len(features) , " is loaded.....")
    # print(features[:100])
    return features

def find_features(w_features, t_words):
    words = t_words
    features = {}
    for f in w_features:
        features[f] = 0

    for f in features:
        if f in words:
            features[f] += 1
    return features

def saperate_training_and_testing_data(dataset):

    # for the 10-fold validation, we devide the whole dataset into 10 segment.
    # print(len(dataset))
    # print(len(dataset[0]))
    #
    # random.shuffle(dataset)
    # total = 1336
    # testing = []
    # training = []
    # for index in range(len(dataset)):
    #     if index < total:
    #         testing.append(dataset[index])
    #     else:
    #         training.append(dataset[index])
    #
    #     # save_documents = open("./T&T/testing.pickle", "wb")
    #     # pickle.dump(testing, save_documents)
    #     # save_documents.close()
    #
    # training_set = []
    # for index in range(10):
    #     if index == 0:
    #         training_set = training[:1200]
    #     elif index == 1:
    #         training_set = training[1200:2400]
    #     elif index == 2:
    #         training_set = training[2400:3600]
    #     elif index == 3:
    #         training_set = training[3600:4800]
    #     elif index == 4:
    #         training_set = training[4800:6000]
    #     elif index == 5:
    #         training_set = training[6000:7200]
    #     elif index == 6:
    #         training_set = training[7200:8400]
    #     elif index == 7:
    #         training_set = training[8400:9600]
    #     elif index == 8:
    #         training_set = training[9600:10800]
    #     elif index == 9:
    #         training_set = training[10800:]
    #     print(len(training_set))
    #
    #     save_documents = open("./T&T/training" + str(index + 1) + ".pickle", "wb")
    #     pickle.dump(training_set, save_documents)
    #     save_documents.close()



def make_featuresets(word_features):

    documents_f = open("./T&T/testing.pickle", "rb")
    testing_files = pickle.load(documents_f)
    documents_f.close()
    print(str(len(testing_files)) + " testing files loaded.....")

    testing_featureset = []

    for index in range(len(testing_files)):
        testing_featureset.append(
            [find_features(word_features, testing_files[index][2]),
             testing_files[index][1]])

    save_featuresets = open("./feature_modeling/testing_featureset.pickle", "wb")
    pickle.dump(testing_featureset, save_featuresets)
    save_featuresets.close()
    print("testing featuresets saved.....")
    print("===============>")

    for t_index in range(10):
        documents_f = open("./T&T/training" + str(t_index + 1) +".pickle", "rb")
        training_files = pickle.load(documents_f)
        documents_f.close()
        print(str(len(training_files)) + " training files loaded.....")

        training_featureset = []

        for index in range(len(training_files)):
            training_featureset.append(
                [find_features(word_features, training_files[index][2]),
                 training_files[index][1]])

        save_featuresets = open("./feature_modeling/training_featureset" + str(t_index + 1) + ".pickle","wb")
        pickle.dump(training_featureset, save_featuresets)
        save_featuresets.close()
        print("training featuresets " + str(t_index + 1) + " saved.....")
        print("===============>")


if __name__ == '__main__':
    # dataset = load_dataset()
    features = load_features()
    # saperate_training_and_testing_data(dataset)
    make_featuresets(features)

