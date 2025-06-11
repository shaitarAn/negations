# !/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import sys
from collections import defaultdict

# python3 read_json_files.py evaluated/ENG2_1878_RUSX.json evaluated/SP2_1878_RUSX.json evaluated/FR2_RUSX.json

infile = sys.argv[1]
infile2 = sys.argv[2]
# infile3 = sys.argv[3]
# outfile = format('combined_evaluation_mBERT.txt')
# prons = format('negPRON_rus.txt')


def find_PRONS(dicts):

    pronoms = []
    with open(prons, 'r') as pronms:
        for s in pronms:
            # print(s)
            pronoms.append(s.strip())

        for k, v in dicts.items():
            if k in pronoms:
                print(k)
                # print(v)
                print('GOLD:', str(v[0]))
                print('SPAN:', str(v[1]))
                print('ENGL:', str(v[2]))
                print('FREN:', str(v[3]))
                print()

    print(len(pronoms), len(dicts))


def pool_anno():

    def all_same(items):
        return all(x == items[0] for x in items)

    annos = defaultdict(list)
    with open(infile) as en, open(infile2) as sp, open(infile3) as fr:
        dataE = json.load(en)
        dataS = json.load(sp)
        dataF = json.load(fr)

        for line in dataS:
            # print(line)
            lang_annos = []
            lang_annos.append(line[2])
            lang_annos.append(line[3])

            for lineE in dataE:
                if lineE[0] == line[0]:
                    lang_annos.append(lineE[3])

            for lineF in dataF:
                if lineF[0] == line[0]:

                    lang_annos.append(lineF[3])

            sent = ' '.join(line[0])
            # print(sent)
            annos[sent] = lang_annos

            # with open(outfile, 'w') as outf:
            #     ideal = 0
            #     for k, v in annos.items():

            # outf.write(k + '\n')
            # outf.write('GOLD:' + str(v[0]) + '\n')
            # outf.write('SPAN:' + str(v[1]) + '\n')
            # outf.write('ENGL:' + str(v[2]) + '\n')
            # outf.write('FREN:' + str(v[3]) + '\n')
            # outf.write('\n')

    return annos


def find_perfect_scopes():
    # python3 read_json_files.py evaluated/mBERT_SP2_1878_RUSX.json evaluated/SP2_1878_RUSX.json

    with open(infile) as bert, open(infile2) as xlm:
        dataB = json.load(bert)
        dataX = json.load(xlm)

        my_dict = defaultdict(list)

        count1 = 0
        count2 = 0

        for line in dataB:
            if line[2] == line[3]:
                # print(line)
                # print()
                my_dict[line[0][0]].append(line[3])
                count2 += 1
                # print(line[0])
                # print()
        for line in dataX:
            # print(line)
            if line[0][0] in my_dict and line[3] != line[2]:
                # print(line[3])
                my_dict[line[0][0]].append(line[3])
                # print()

        sent = 0
        for k, v in my_dict.items():

            if len(v) > 1:
                sent += 1
                tokens = k.split()
                scopes = [(i[0], i[1], i[2]) for i in zip(tokens, v[0], v[1])]
                print(sent, k)
                print(v[0])
                # print(scopes)
                for i in scopes:
                    if int(i[1]) != i[2]:
                        print(i)
                # print(v[0])
                # print(v[1])
                print()

        print(len(my_dict))

        print('BERT:', count1, len(dataB), round(count1/len(dataB)*100, 2))
        print('XLM-R', count2, len(dataX), round(count2/len(dataX)*100, 2))


def find_diff_between_models():

    with open(infile) as bert, open(infile2) as xlm, open(outfile, 'w') as outf:
        dataB = json.load(bert)
        dataX = json.load(xlm)

        count = 0
        for line in dataB:
            for line2 in dataX:
                if line[0][0].split()[:3] == line2[0][0].split()[:3] and line[2] != line2[2] and line2[1] == line2[2]:
                    count += 1
                    # outf.write(line[0][0] + '\n')
                    # outf.write(str(line[1]) + '\n')
                    # outf.write(str(line[2]) + '\n')
                    # outf.write(str(line2[2]) + '\n')
                    # outf.write('\n')

                    print(line[0])
                    print(line[1])
                    print('-----------')
                    print(line[2])
                    print(line2[2])
                    print()

        print(count)


# my_dict = pool_anno()
# find_PRONS(my_dict)
# find_perfect_scopes()

# find_diff_between_models()


# for line in data:
#     # print(line)
#     outf.write(' '.join(line[0]) + '\n')
# cue = ''
# true_scope = ''
# bert_scope = ''
# outf.write(str(lines) + '\n')
# outf.write(' '.join(line[0]) + '\n')
# outf.write('CUE:  ' + str(line[1]) + '\n')
# outf.write('TRUE: ' + str(line[2]) + '\n')
# outf.write('BERT: ' + str(line[3]) + '\n')
# zipped = zip(line[0], line[1], line[2], line[3])
# for i in zipped:
#     if i[1] == 2:
#         cue += i[0] + ' '
#     elif i[1] == 1:
#         cue = i[0]
#     if i[2] == 1:
#         true_scope += i[0] + ' '
#     if i[3] == 1:
#         bert_scope += i[0] + ' '
# outf.write('Q:' + cue.strip() + '\n')
# outf.write('TRUE: ' + true_scope.strip() + '\n')
# outf.write('BERT: ' + bert_scope.strip() + '\n')
# outf.write('\n')
# lines += 1
