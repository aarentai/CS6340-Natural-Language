import sys


def sentiment(arg):
    train_file = arg[1]
    test_file = arg[2]
    features_files = arg[3]
    k = int(arg[4])

    with open(train_file) as f:
        train_text = [word.rstrip() for word in f]
    train_text.append('')

    with open(test_file) as f:
        test_text = [word.rstrip() for word in f]
    test_text.append('')

    with open(features_files) as f:
        words = [word.rstrip() for word in f]

    # train
    with open('trainS.txt.vector', "w") as f:
        f.write('')
    interval_id = [i for i, x in enumerate(train_text) if x == '']

    for i in range(len(interval_id)):
        if i == 0:
            start = 0
            end = interval_id[i]
        else:
            start = interval_id[i-1]+1
            end = interval_id[i]

        feature_id_list = []
        for j in range(start+1, end):
            if train_text[j] in words[:k] and words.index(train_text[j]) not in feature_id_list:
                feature_id_list.append(words.index(train_text[j]))
        feature_id_list.sort()

        with open('trainS.txt.vector', "a") as f:
            f.write(train_text[start])

        for j in range(len(feature_id_list)):
            with open('trainS.txt.vector', "a") as f:
                feature_id = feature_id_list[j]+1
                f.write(" "+str(feature_id)+":1")

        with open('trainS.txt.vector', "a") as f:
            f.write('\n')

    # test
    with open('testS.txt.vector', "w") as f:
        f.write('')
    interval_id = [i for i, x in enumerate(test_text) if x == '']

    for i in range(len(interval_id)):
        if i == 0:
            start = 0
            end = interval_id[i]
        else:
            start = interval_id[i-1]+1
            end = interval_id[i]

        feature_id_list = []
        for j in range(start+1, end):
            if test_text[j] in words[:k] and words.index(test_text[j]) not in feature_id_list:
                feature_id_list.append(words.index(test_text[j]))
        feature_id_list.sort()

        with open('testS.txt.vector', "a") as f:
            f.write(test_text[start])

        for j in range(len(feature_id_list)):
            with open('testS.txt.vector', "a") as f:
                feature_id = feature_id_list[j]+1
                f.write(" "+str(feature_id)+":1")

        with open('testS.txt.vector', "a") as f:
            f.write('\n')


if __name__ == "__main__":
    sentiment(sys.argv)
    # sentiment(['sentiment.py', 'trainS.txt', 'testS.txt', 'words.txt', '100'])
