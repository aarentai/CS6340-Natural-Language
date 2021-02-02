import sys
import numpy as np


def cos_sim(x, y):
    if (np.linalg.norm(x) * np.linalg.norm(y)) != 0:
        return np.inner(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    else:
        return 0


def any_alpha(word):
    for s in word:
        if s.isalpha():
            return True
    return False


def not_only(word, window):
    for i in range(len(window)):
        window[i] = window[i].lower()
    if window.count(word) > 1:
        return True
    return False


def distsim(arg):
    train_file = arg[1]
    test_file = arg[2]
    stopwords_file = arg[3]
    k = int(arg[4])
    output_file = test_file + '.distsim'

    '''train'''
    with open(train_file) as f:
        train_list = [word.rstrip() for word in f]
    with open(test_file) as f:
        test_list = [word.rstrip() for word in f]
    with open(stopwords_file) as f:
        stopwords_list = [word.rstrip() for word in f]

    vocabulary_list = []
    sense_list = []
    window_set = []
    for i in range(len(train_list)):
        train_list[i] = train_list[i].replace('\t', ' ')
        temp_train = list(filter(lambda word: word != '', train_list[i].split(' ')))
        target_word_pos = 1
        for j in range(len(temp_train)):
            if '<occurrence>' in temp_train[j]:
                target_word_pos = j
        sense_list.append(temp_train[0].replace('GOLDSENSE:', ''))
        if k != 0:
            window = temp_train[max(target_word_pos - k, 1):target_word_pos] + \
                     temp_train[target_word_pos + 1:min(target_word_pos + k + 1, len(temp_train))]
        else:
            window = temp_train[1:target_word_pos] + temp_train[target_word_pos + 1:]
        window = [word.lower() for word in window]
        vocabulary_list.append(window)
        window_set = window_set + window

    distinct_sense_list = list(set(sense_list))
    combined_vocabulary_list = list(set([word for word in window_set if window_set.count(
        word.lower()) != 1 and word not in stopwords_list and any_alpha(word)]))
    signature_vector = np.zeros((len(distinct_sense_list), len(combined_vocabulary_list)))
    for i in range(len(vocabulary_list)):
        for j in range(len(vocabulary_list[i])):
            if vocabulary_list[i][j] in combined_vocabulary_list:
                signature_vector[
                    distinct_sense_list.index(sense_list[i]), combined_vocabulary_list.index(
                        vocabulary_list[i][j])] += 1

    '''test'''
    context_vector = np.zeros((len(test_list), len(combined_vocabulary_list)))
    for i in range(len(test_list)):
        temp_context = list(filter(lambda word: word != '', test_list[i].split(' ')))
        target_word_pos = 0
        for j in range(len(temp_context)):
            if '<occurrence>' in temp_context[j]:
                target_word_pos = j
        if k != 0:
            window = temp_context[max(target_word_pos - k, 0):target_word_pos] + \
                     temp_context[target_word_pos + 1:min(target_word_pos + k + 1, len(temp_context))]
        else:
            window = temp_context[:target_word_pos] + temp_context[target_word_pos + 1:]
        window = [word.lower() for word in window]  #
        for m in range(len(window)):
            if window[m] in combined_vocabulary_list:
                context_vector[i, combined_vocabulary_list.index(window[m])] += 1

    with open(output_file, "w") as f:
        f.write('Number of Training Sentences = ' + str(len(train_list)) + '\n')
        f.write('Number of Test Sentences = ' + str(len(test_list)) + '\n')
        f.write('Number of Gold Senses = ' + str(len(distinct_sense_list)) + '\n')
        f.write('Vocabulary Size = ' + str(len(combined_vocabulary_list)) + '\n')

    for i in range(len(test_list)):
        score = []
        for j in range(len(distinct_sense_list)):
            score.append(cos_sim(context_vector[i, :], signature_vector[j, :]))

        sense_n_score = list(zip(score, distinct_sense_list))
        sense_n_score = sorted(sense_n_score, key=lambda x: (-x[0], x[1]))

        for j in range(len(distinct_sense_list)):
            with open(output_file, "a") as f:
                f.write(sense_n_score[j][1] + '(' + str(format(sense_n_score[j][0], '.2f')) + ') ')

        with open(output_file, "a") as f:
            f.write('\n')


if __name__ == "__main__":
    distsim(sys.argv)
    # distsim(['distsim.py', 'train.txt', 'test.txt', 'stopwords.txt', '0'])
