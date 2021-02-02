import sys


def class_to_id(class_label):
    switcher = {
        'O': 0,
        'B-PER': 1,
        'I-PER': 2,
        'B-LOC': 3,
        'L-LOC': 4,
        'B-ORG': 5,
        'I-ORG': 6
    }
    return switcher.get(class_label, 0)


def is_abbr(word):
    if word[-1]=='.' and len(word)<=4:
        word = word.replace('.','')
        if word.isalpha():
            return True

    return False


def entities(arg):
    train_file = arg[1]
    test_file = arg[2]
    feature = arg[3:]
    with open(train_file) as f:
        train_text = [word.rstrip() for word in f]
    train_text.append('')

    with open(test_file) as f:
        test_text = [word.rstrip() for word in f]
    test_text.append('')

    POS_id_list = []
    WORD_id_list = []
    WORDCON_id_list = []
    POSCON_id_list = []
    full_feature_id_list = []

    '''
    Create full_feature_id_list
    '''
    for i in range(len(train_text)):
        if train_text[i] != '':
            if i > 0 and train_text[i-1] != '':
                prev_word_info = train_text[i-1].split(' ')
                prev_word_info = list(filter(lambda a: a != '', prev_word_info))
                prev_pos = 'prev-pos-' + prev_word_info[1]
                if prev_pos not in POSCON_id_list:
                    POSCON_id_list.append(prev_pos)
                prev_word = 'prev-word-' + prev_word_info[2]
                if prev_word not in WORDCON_id_list:
                    WORDCON_id_list.append(prev_word)

            if i < len(train_text) - 1 and train_text[i+1] != '':
                next_word_info = train_text[i+1].split(' ')
                next_word_info = list(filter(lambda a: a != '', next_word_info))
                # print(next_word_info)
                next_pos = 'next-pos-' + next_word_info[1]
                if next_pos not in POSCON_id_list:
                    POSCON_id_list.append(next_pos)
                next_word = 'next-word-' + next_word_info[2]
                if next_word not in WORDCON_id_list:
                    WORDCON_id_list.append(next_word)

            word_info = train_text[i].split(' ')
            word_info = list(filter(lambda a: a != '', word_info))
            if word_info[1] not in POS_id_list:
                POS_id_list.append(word_info[1])
            if word_info[2] not in WORD_id_list:
                WORD_id_list.append(word_info[2])

    WORD_id_list.append('UNK')
    POS_id_list.append('UNKPOS')
    WORDCON_id_list.extend(['prev-word-PHI','next-word-OMEGA'])
    POSCON_id_list.extend(['prev-pos-PHIPOS','next-pos-OMEGAPOS'])

    full_feature_id_list = full_feature_id_list + WORD_id_list
    if 'POS' in feature:
        full_feature_id_list = full_feature_id_list+POS_id_list
    if 'POSCON' in feature:
        full_feature_id_list = full_feature_id_list+POSCON_id_list
    if 'WORDCON' in feature:
        full_feature_id_list = full_feature_id_list+WORDCON_id_list
    if 'ABBR' in feature:
        full_feature_id_list = full_feature_id_list+['-ABBR-']
    if 'CAP' in feature:
        full_feature_id_list = full_feature_id_list+['-CAP-']

    with open('full_feature_id_list.txt','w') as f:
        for element in full_feature_id_list:
            f.write(element)
            f.write('\n')

    '''
    Create feature for each sentence in TRAIN
    '''
    with open('trainE.txt.readable', "w") as f:
        f.write('')
    with open('trainE.txt.vector', "w") as f:
        f.write('')
    interval_id = [i for i, x in enumerate(train_text) if x == '']

    for i in range(len(interval_id)):
        if i == 0:
            start = 0
            end = interval_id[i]
        else:
            start = interval_id[i-1]+1
            end = interval_id[i]

        for j in range(start, end):
            word_info = list(filter(lambda a: a != '', train_text[j].split(' ')))

            if j-1 >= 0 and train_text[j-1] != '':
                prev_word_info = list(filter(lambda a: a != '', train_text[j-1].split(' ')))
            else:
                prev_word_info = ['O','PHIPOS','PHI']

            if j+1 < len(train_text) and train_text[j+1] != '':
                next_word_info = list(filter(lambda a: a != '', train_text[j+1].split(' ')))
            else:
                next_word_info = ['O','OMEGAPOS','OMEGA']

            # readable output file
            with open('trainE.txt.readable', "a") as f:
                f.write('WORD: '+word_info[2]+'\n')

                if 'POS' in feature:
                    f.write('POS: '+word_info[1]+'\n')
                else:
                    f.write('POS: n/a\n')

                if 'ABBR' in feature:
                    if is_abbr(word_info[2]):
                        f.write('ABBR: yes\n')
                    else:
                        f.write('ABBR: no\n')
                else:
                    f.write('ABBR: n/a\n')

                if 'CAP' in feature:
                    if word_info[2][0].isupper():
                        f.write('CAP: yes\n')
                    else:
                        f.write('CAP: no\n')
                else:
                    f.write('CAP: n/a\n')

                if 'WORDCON' in feature:
                    f.write('WORDCON: '+prev_word_info[2]+' '+next_word_info[2]+'\n')
                else:
                    f.write('WORDCON: n/a\n')

                if 'POSCON' in feature:
                    f.write('POSCON: '+prev_word_info[1]+' '+next_word_info[1]+'\n')
                else:
                    f.write('POSCON: n/a\n')

                f.write('\n')

            # feature vector output file
            feature_id_list = []
            # word
            if word_info[2] in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(word_info[2]))

            # pos
            if 'POS' in feature and word_info[1] in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(word_info[1]))

            # abbr
            if 'ABBR' in feature and is_abbr(word_info[2]):
                feature_id_list.append(full_feature_id_list.index('-ABBR-'))

            # cap
            if 'CAP' in feature and word_info[2][0].isupper():
                feature_id_list.append(full_feature_id_list.index('-CAP-'))

            # wordcon
            prev_word = 'prev-word-' + prev_word_info[2]
            if 'WORDCON' in feature and prev_word in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(prev_word))
            next_word = 'next-word-' + next_word_info[2]
            if 'WORDCON' in feature and next_word in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(next_word))

            # poscon
            prev_pos = 'prev-pos-' + prev_word_info[1]
            if 'POSCON' in feature and prev_pos in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(prev_pos))
            next_pos = 'next-pos-' + next_word_info[1]
            if 'POSCON' in feature and next_pos in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(next_pos))

            feature_id_list = list(set(feature_id_list))
            feature_id_list.sort()

            with open('trainE.txt.vector',"a") as f:
                f.write(str(class_to_id(word_info[0])))

            for k in range(len(feature_id_list)):
                with open('trainE.txt.vector', "a") as f:
                    feature_id = feature_id_list[k]+1
                    f.write(" "+str(feature_id)+":1")

            with open('trainE.txt.vector', "a") as f:
                f.write('\n')


    '''
    Create feature for each sentence in TEST
    '''
    with open('testE.txt.readable', "w") as f:
        f.write('')
    with open('testE.txt.vector', "w") as f:
        f.write('')
    interval_id = [i for i, x in enumerate(test_text) if x == '']

    for i in range(len(interval_id)):
        if i == 0:
            start = 0
            end = interval_id[i]
        else:
            start = interval_id[i-1]+1
            end = interval_id[i]

        for j in range(start, end):
            word_info = list(filter(lambda a: a != '', test_text[j].split(' ')))

            if j-1 >= 0 and test_text[j-1] != '':
                prev_word_info = list(filter(lambda a: a != '', test_text[j-1].split(' ')))
                if prev_word_info[1] not in POS_id_list:
                    prev_word_info[1] = 'UNKPOS'
                if prev_word_info[2] not in WORD_id_list:
                    prev_word_info[2] = 'UNK'
            else:
                prev_word_info = ['O','PHIPOS','PHI']

            if j+1 < len(test_text) and test_text[j+1] != '':
                next_word_info = list(filter(lambda a: a != '', test_text[j+1].split(' ')))
                if next_word_info[1] not in POS_id_list:
                    next_word_info[1] = 'UNKPOS'
                if next_word_info[2] not in WORD_id_list:
                    next_word_info[2] = 'UNK'
            else:
                next_word_info = ['O','OMEGAPOS','OMEGA']

            # readable output file
            with open('testE.txt.readable', "a") as f:
                f.write('WORD: '+word_info[2]+'\n')

                if 'POS' in feature:
                    f.write('POS: '+word_info[1]+'\n')
                else:
                    f.write('POS: n/a\n')

                if 'ABBR' in feature:
                    if is_abbr(word_info[2]):
                        f.write('ABBR: yes\n')
                    else:
                        f.write('ABBR: no\n')
                else:
                    f.write('ABBR: n/a\n')

                if 'CAP' in feature:
                    if word_info[2][0].isupper() and word_info[2] != 'UNK':
                        f.write('CAP: yes\n')
                    else:
                        f.write('CAP: no\n')
                else:
                    f.write('CAP: n/a\n')

                if 'WORDCON' in feature:
                    f.write('WORDCON: '+prev_word_info[2]+' '+next_word_info[2]+'\n')
                else:
                    f.write('WORDCON: n/a\n')

                if 'POSCON' in feature:
                    f.write('POSCON: '+prev_word_info[1]+' '+next_word_info[1]+'\n')
                else:
                    f.write('POSCON: n/a\n')

                f.write('\n')

            # feature vector output file
            feature_id_list = []
            # word
            if word_info[2] in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(word_info[2]))
            else:
                feature_id_list.append(full_feature_id_list.index('UNK'))

            # pos
            if 'POS' in feature:
                if word_info[1] in full_feature_id_list:
                    feature_id_list.append(full_feature_id_list.index(word_info[1]))
                else:
                    feature_id_list.append(full_feature_id_list.index('UNKPOS'))

            # abbr
            if 'ABBR' in feature and is_abbr(word_info[2]):
                feature_id_list.append(full_feature_id_list.index('-ABBR-'))

            # cap
            if 'CAP' in feature and word_info[2][0].isupper():
                feature_id_list.append(full_feature_id_list.index('-CAP-'))

            # wordcon
            prev_word = 'prev-word-' + prev_word_info[2]
            if 'WORDCON' in feature and prev_word in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(prev_word))
            next_word = 'next-word-' + next_word_info[2]
            if 'WORDCON' in feature and next_word in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(next_word))

            # poscon
            prev_pos = 'prev-pos-' + prev_word_info[1]
            if 'POSCON' in feature and prev_pos in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(prev_pos))
            next_pos = 'next-pos-' + next_word_info[1]
            if 'POSCON' in feature and next_pos in full_feature_id_list:
                feature_id_list.append(full_feature_id_list.index(next_pos))

            feature_id_list = list(set(feature_id_list))
            feature_id_list.sort()

            with open('testE.txt.vector', "a") as f:
                f.write(str(class_to_id(word_info[0])))

            for k in range(len(feature_id_list)):
                with open('testE.txt.vector', "a") as f:
                    feature_id = feature_id_list[k]+1
                    f.write(" "+str(feature_id)+":1")

            with open('testE.txt.vector', "a") as f:
                f.write('\n')


if __name__ == "__main__":
    entities(sys.argv)
    # entities(['entities.py', 'trainE.txt', 'testE.txt', 'WORD', 'CAP', 'POS', 'POSCON', 'WORDCON', 'ABBR'])
