import pandas as pd
import pickle




if __name__ == '__main__':

    # dataset = []
    #
    # df_text = pd.read_csv('./dataset/TextPreprocessed.csv', encoding='iso-8859-1')
    # # print(df_text.head())
    # df_tags = pd.read_csv('./dataset/Tag.csv', encoding='iso-8859-1')
    # # print(df_tags.head())
    #
    # # grouped_tags = df_tags.groupby("Tag", sort='count').size().reset_index(name='count')
    # # fig = plt.figure(figsize=(12,10))
    # # grouped_tags.plot(figsize=(12,7), title="Tag frequency")
    # # plt.show()
    #
    # num_classes = 14
    # grouped_tags = df_tags.groupby("Tag").size().reset_index(name='count')
    # most_common_tags = grouped_tags.nlargest(num_classes, columns="count")
    # df_tags.Tag = df_tags.Tag.apply(lambda tag: tag if tag in most_common_tags.Tag.values else None)
    # df_tags = df_tags.dropna()
    #
    # counts = df_tags.Tag.value_counts()
    # firstlast = counts[:5].append(counts[-5:])
    # firstlast.reset_index(name="count")
    #
    # # print(firstlast)
    #
    # def tags_for_question(question_id):
    #     return df_tags[df_tags['Id'] == question_id].Tag.values
    #
    #
    # def add_tags_column(row):
    #     row['Tags'] = tags_for_question(row['Id'])
    #     return row
    #
    # df_questions = df_text.apply(add_tags_column, axis=1)
    #
    # for index, row in df_questions.iterrows():
    #     dataset.append([row['Text'], row['Tags']])
    #
    # f = open('./dataset/final_dataset.pickle', 'wb')
    # pickle.dump(dataset,f)
    # f.close()
    # print("dataset saved.....")
    # print('==========>')

    f = open('./dataset/final_dataset.pickle', 'rb')
    dataset = pickle.load(f)
    f.close()
    print("dataset laoded.....")
    print('==========>')


    binary_class_dataset = []
    for index in range(len(dataset)):
        task = []
        task.append(dataset[index][0])
        if str(dataset[index][1][0]).strip() == 'none':
            ref = 0
        else:
            ref = 1
        task.append(ref)

        binary_class_dataset.append(task)

    f = open('./dataset/binary_class_dataset.pickle', 'wb')
    pickle.dump(binary_class_dataset,f)
    f.close()
    print("dataset saved.....")
    print('==========>')

    print(binary_class_dataset[0])
