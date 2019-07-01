import pickle
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import re
from collections import Counter
import string
import numpy as np
import math

def clean_text(text):
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    text.lower();
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character): None for character in nonprintable})

def tokenization(text):
    return word_tokenize(text)

def pos_tagging(text):

    return pos_tag(text)

def lemmatization(pos_tags):
    adjective_tags = ['JJ', 'JJR', 'JJS']
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_text = []
    for word in pos_tags:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0], pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0])))  # default POS = noun
    return lemmatized_text

def stop_word_removal(pos_tags_lem, lem_text):
    stopwords = []

    wanted_POS = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBG', 'FW']

    for word in pos_tags_lem:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])

    punctuations = list(str(string.punctuation))

    stopwords = stopwords + punctuations

    stopword_file = open("./dataset/long_stopwords.txt", "r")
    # Source = https://www.ranks.nl/stopwords

    lots_of_stopwords = []

    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))

    stopwords_plus = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)

    processed_text = []
    for word in lem_text:
        if word not in stopwords_plus:
            processed_text.append(word)

    return processed_text, stopwords_plus

if __name__ == '__main__':
    load = open("dataset/binary_class_dataset.pickle", "rb")
    tasks = pickle.load(load)
    load.close()
    print(tasks[0])
    print("tasks loaded.....")

    preprocessed_tasks = []

    all_words = []
    freq_words_without_freq = []

    for index in range(len(tasks)):

        # without preprocessing
        old_task = tasks[index]
        text = tasks[index][0].lower()
        cleaned_text = clean_text(text)
        words = re.findall(r'\w+', cleaned_text)

        # with preprocessing
        # old_task = tasks[index]
        # text = tasks[index][0].lower()
        # print(text)
        # cleaned_text = clean_text(text)
        # print(cleaned_text)
        # token_text = tokenization(cleaned_text)
        # print(token_text)
        # pos_tag_text = pos_tagging(token_text)
        # # print(pos_tag_text)
        # lem_text = lemmatization(pos_tag_text)
        # # print(lem_text)
        # pos_tag_lem_text = pos_tagging(lem_text)
        # # print(pos_tag_lem_text)
        # processed_text, stopwords_plus = stop_word_removal(pos_tag_lem_text, lem_text)
        # # print(processed_text)

        # # with preprocessing
        # for item in processed_text:

        # without preprocessing
        for item in words:

            all_words.append(item)

        # old_task = list(tasks[index])
        # old_task.append(processed_text)
        # preprocessed_tasks.append(old_task)

    counts = Counter(all_words).most_common(5000)

    for index in range(len(counts)):
        freq_words_without_freq.append(counts[index][0])

    # file = open("./dataset/freq_words_with_freq.pickle","wb")
    # pickle.dump(counts, file)
    # file.close()
    # print("all_phrases_with_freq saved......")

    file = open("./dataset/freq_words_without_preprocessing.pickle", "wb")
    pickle.dump(freq_words_without_freq, file)
    file.close()
    print("all_phrases_without_freq saved......")

    # file = open("./dataset/final_dataset_preprocessed.pickle", "wb")
    # pickle.dump(preprocessed_tasks, file)
    # file.close()
    # print("final_dateset_with_phrases saved......")
