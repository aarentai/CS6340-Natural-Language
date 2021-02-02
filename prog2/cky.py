import sys


class cell:
    def __init__(self, constituent_and_probability):
        self.CnP = constituent_and_probability


def find_feasible_grammar(cell1, cell2, grammar):
    CnP = []
    for i in range(len(cell1.CnP)):
        for j in range(len(cell2.CnP)):
            for k in range(len(grammar)):
                if len(grammar[k]) == 4 and cell1.CnP[i]['constituent'] == grammar[k][1] and cell2.CnP[j]['constituent'] == grammar[k][2]:
                    CnP.append({'constituent': grammar[k][0],
                                'probability': float(grammar[k][-1]) * cell1.CnP[i]['probability'] * cell2.CnP[j]['probability']})

    return CnP

def cky(arg):
    pcfg_file = arg[1]
    sentences_file = arg[2]
    if len(arg) == 4:
        prob_flag = arg[3]
        output_file_name = sentences_file + '.probcky'
    else:
        prob_flag = ''
        output_file_name = sentences_file + '.cky'

    with open(pcfg_file) as f:
        pcfg = [word.rstrip() for word in f]

    # store pcfg in the grammar list
    grammars_list = []
    for i in range(len(pcfg)):
        pcfg[i] = pcfg[i].replace('-> ', '')
        grammars_list.append(list(filter(lambda a: a != '', pcfg[i].split(' '))))
    # print(grammars_list)

    # store sentences in the list
    with open(sentences_file) as f:
        sentences_list = [word.rstrip() for word in f]

    with open(output_file_name, "w") as f:
        f.write('')

    # pick up one sentence in sentences list
    for i in range(len(sentences_list)):
        # store words in the sentence in words_list
        words_list = list(filter(lambda a: a != '', sentences_list[i].split(' ')))

        # build table
        l = len(words_list)
        table = [[] for j in range(l)]
        for j in range(l):
            for k in range(l):
                table[j].append(cell([]))

        # fill the diagonal
        for j in range(l):
            for k in range(len(grammars_list)):
                if words_list[j] in grammars_list[k]:
                    table[j][j].CnP.append({'constituent':grammars_list[k][0],
                                            'probability':float(grammars_list[k][-1])})

        # fill the cell[k, j]
        for j in range(1, l):
            for k in range(j-1, -1, -1):
                for m in range(k, j):
                    new_CnP = find_feasible_grammar(table[k][m], table[m + 1][j], grammars_list)
                    table[k][j].CnP += new_CnP

        with open(output_file_name, "a") as f:
            f.write('PARSING SENTENCE: '+sentences_list[i]+'\n')
            f.write('NUMBER OF PARSES FOUND: '+str(len(set([c['constituent'] for c in table[0][l-1].CnP])))+'\n')
            f.write('TABLE: \n')

        for k in range(l):
            for j in range(k, l):
                with open(output_file_name, "a") as f:
                    f.write('cell['+str(k+1)+','+str(j+1)+']: ')

                # keep the max prob in each constituent
                unique_CnP = []
                for m in set([dict['constituent'] for dict in table[k][j].CnP]):
                    dict_of_same_constituend = [dict for dict in table[k][j].CnP if dict["constituent"] == m]
                    unique_CnP.append({'constituent': m,
                                       'probability': max([c['probability'] for c in dict_of_same_constituend])})
                table[k][j].CnP = unique_CnP
                table[k][j].CnP = sorted(table[k][j].CnP, key=lambda k: k['constituent'])

                if len(table[k][j].CnP) == 0:
                    with open(output_file_name, "a") as f:
                        f.write('-')
                else:
                    for m in range(len(table[k][j].CnP)):
                        with open(output_file_name, "a") as f:
                            if prob_flag == '-prob':
                                f.write(table[k][j].CnP[m]['constituent']+'('+str(format(table[k][j].CnP[m]['probability'], '.4f'))+') ')
                            else:
                                f.write(table[k][j].CnP[m]['constituent'] + ' ')

                with open(output_file_name, "a") as f:
                    f.write('\n')

        with open(output_file_name, "a") as f:
            f.write('\n')


if __name__ == "__main__":
    cky(sys.argv)
    # cky(['cky.py', 'pcfg-example.txt', 'sentences-example.txt'])

