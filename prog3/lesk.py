import sys
import numpy as np

def any_alpha(word):
    for s in word:
        if s.isalpha():
            return True
    return False


def comp_overlap(signature, context):
    overlap = [word for word in context if word in signature]
    return len(overlap)


def lesk(arg):
    test_file = arg[1]
    definitions_file = arg[2]
    stopwords_file = arg[3]
    output_file = test_file + '.lesk'
    with open(test_file) as f:
        test_list = [word.rstrip() for word in f]
    with open(definitions_file) as f:
        definitions_list = [word.rstrip() for word in f]
    with open(stopwords_file) as f:
        stopwords_list = [word.rstrip() for word in f]

    signature_list = []
    distinct_sense_list = []
    for i in range(len(definitions_list)):
        definitions_list[i] = definitions_list[i].replace('\t', ' ')
        temp_signature = list(filter(lambda word: word != '', definitions_list[i].split(' ')))
        distinct_sense_list.append(temp_signature[0])
        temp_signature = temp_signature[1:]
        temp_signature = [word.lower() for word in temp_signature if word not in stopwords_list and any_alpha(word)]
        signature_list.append(temp_signature)
    # print(signature_list)

    context_list = []
    for i in range(len(test_list)):
        temp_context = list(set(list(filter(lambda word: word != '', test_list[i].split(' ')))))
        temp_context = [word.lower() for word in temp_context if word not in stopwords_list and any_alpha(word)]
        context_list.append(temp_context)

    with open(output_file, "w") as f:
        f.write('')

    for i in range(len(test_list)):
        score = []
        for j in range(len(signature_list)):
            score.append(comp_overlap(signature_list[j], context_list[i]))

        sense_n_score = list(zip(score, distinct_sense_list))
        sense_n_score = sorted(sense_n_score, key=lambda x: (-x[0], x[1]))
        for j in range(len(signature_list)):
            with open(output_file, "a") as f:
                f.write(sense_n_score[j][1] + '(' + str(sense_n_score[j][0]) + ') ')

        with open(output_file, "a") as f:
            f.write('\n')


if __name__ == "__main__":
    lesk(sys.argv)
    # lesk(['lesk.py', 'test.txt', 'definitions.txt', 'stopwords.txt'])
