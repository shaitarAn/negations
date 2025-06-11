# !/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Extracts tokens and annotations from the original corpus,
removes odd quotation marks, creates a json file that is suitable for NegBERT.
'''

from collections import defaultdict
from pathlib import Path
import json

data1 = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_Sherlock_dataset/cd-sco/corpus/test-gold/SEM-2012-SharedTask-CD-SCO-test-cardboard-GOLD.txt'
data2 = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_Sherlock_dataset/cd-sco/corpus/test-gold/SEM-2012-SharedTask-CD-SCO-test-circle-GOLD.txt'
data3 = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_Sherlock_dataset/cd-sco/corpus/training/SEM-2012-SharedTask-CD-SCO-training-09032012.txt'
data4 = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_Sherlock_dataset/cd-sco/corpus/dev/SEM-2012-SharedTask-CD-SCO-dev-09032012.txt'
data = [data1, data2, data3, data4]


def starsem(f_path, cue_sents_only=False, frac_no_cue_sents=1.0):
    '''
    Function taken from NegBERT by Khandelwal et. al
    '''
    all_cues = defaultdict(list)
    raw_data = open(f_path)
    sentence = []
    label = []
    scope_sents = []
    data_scope = []
    scope = []
    scope_cues = []
    cue_only_data = []

    for line in raw_data:
        label = []
        sentence = []
        tokens = line.strip().split()
        # print('tokens', tokens)
        if len(tokens) == 8:  # This line has no cues
            # append the word
            sentence.append(tokens[3])
            label.append(3)  # Not a cue
            for line in raw_data:
                tokens = line.strip().split()
                if len(tokens) == 0:
                    break
                else:
                    sentence.append(tokens[3])
                    label.append(3)
            cue_only_data.append([sentence, label])

        else:
            # The line has 1 or more cues
            num_cues = (len(tokens) - 7) // 3
            scope = [[] for i in range(num_cues)]
            # First list is the real labels, second list is to modify if it is a multi-word cue.
            label = [[], []]
            label[0].append(3)  # Generally not a cue, if it is will be set ahead.
            label[1].append(-1)  # Since not a cue, for now.
            for i in range(num_cues):
                if tokens[7 + 3 * i] != '_':  # Cue field is active
                    if tokens[3] != tokens[7 + 3 * i]:
                        all_cues[tokens[7 + 3 * i]].append(tokens[3])
                    if tokens[8 + 3 * i] != '_':  # Check for affix
                        label[0][-1] = 0  # Affix
                        label[1][-1] = i  # Cue number
                    else:
                        # Maybe a normal or multiword cue. The next few words will determine which.
                        label[0][-1] = 1
                        label[1][-1] = i  # Which cue field, for multiword cue altering.

                if tokens[8 + 3 * i] != '_':
                    scope[i].append(1)
                else:
                    # print(scope[i])
                    scope[i].append(0)
            sentence.append(tokens[3])
            for line in raw_data:
                tokens = line.strip().split()
                if len(tokens) == 0:
                    break
                else:
                    sentence.append(tokens[3])
                    label[0].append(3)  # Generally not a cue, if it is will be set ahead.
                    label[1].append(-1)  # Since not a cue, for now.
                    # print(label[0])
                    for i in range(num_cues):
                        if tokens[7 + 3 * i] != '_':  # Cue field is active
                            if tokens[3] != tokens[7 + 3 * i]:
                                all_cues[tokens[7 + 3 * i]].append(tokens[3])
                            if tokens[8 + 3 * i] != '_':  # Check for affix
                                label[0][-1] = 0  # Affix
                                label[1][-1] = i  # Cue number
                            else:
                                # Maybe a normal or multiword cue. The next few words will determine which.
                                label[0][-1] = 1
                                label[1][-1] = i  # Which cue field, for multiword cue altering.
                        if tokens[8 + 3 * i] != '_':
                            scope[i].append(1)
                        else:
                            scope[i].append(0)
            for i in range(num_cues):
                indices = [index for index, j in enumerate(label[1]) if i == j]
                count = len(indices)
                if count > 1:
                    for j in indices:
                        label[0][j] = 2
            for i in range(num_cues):
                sc = []
                for a, b in zip(label[0], label[1]):
                    if i == b:
                        sc.append(a)

                    else:
                        sc.append(3)
                scope_cues.append(sc)
                scope_sents.append(sentence)
                data_scope.append(scope[i])

    return scope_sents, scope_cues, data_scope


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('SHERLOCK_3labels.json')
    textfile1 = outpath / Path('SHERLOCK_sents.txt')
    textfile2 = outpath / Path('SHERLOCK_3labels_anno.txt')

    json_data = [item[:3] for item in data]

    with open(outfile1, 'w') as outf1:
        json.dump(json_data, outf1)

    with open(textfile1, 'w', encoding='utf8') as outf:
        for item in data:
            outf.write(' '.join(item[0]) + '\n')

    count = 0
    with open(textfile2, 'w', encoding='utf8') as outf:
        for item in data:
            zipped = zip(item[0], item[1], item[2])
            cue = ''
            scope = ''
            for t in zipped:
                if t[1] != 3:
                    cue += ' ' + str(t[0])
                if t[2] != 0:
                    scope += ' ' + str(t[0])
            count += 1
            outf.write(str(count) + '\t' + str(item[3]) + '\n')
            outf.write(' '.join(item[0]) + '\n')
            outf.write(str(item[1]) + '\n')
            outf.write(str(item[2]) + '\n')
            outf.write(cue.strip() + '\n')
            outf.write(scope.strip() + '\n')
            outf.write('\n')


def postprocess(zipped_data):
    newzippy = []
    dataout = []
    for item in zipped_data:
        zippy = zip(item[0], item[1], item[2])

        # remove unconventional quotation marks
        newzippy = [i for i in zippy if i[0] not in ['``', "'", "''", "`"]]

        # reconstruct the data for json
        newlist = []
        for i in zip(*newzippy):
            newlist.append(list(i))
        newlist.append(item[3])

        dataout.append(newlist)

    return dataout


scope_sents = []
scope_cues = []
data_scope = []
files = []

for file in data:

    sents, cues, scopes = starsem(file)
    scope_sents.extend(sents)
    scope_cues.extend(cues)
    data_scope.extend(scopes)
    print(len(sents), file)
    if 'training' in file:
        print(file)
        files.extend(['training_data'] * len(sents))
    if 'cardboard' in file:
        files.extend(['test_data: cardboard'] * len(sents))
    if 'circle' in file:
        files.extend(['test_data: circle'] * len(sents))
    if 'dev-09032012' in file:
        files.extend(['development_data'] * len(sents))

zipped_data = zip(scope_sents, scope_cues, data_scope, files)

dataout = postprocess(zipped_data)
write_files(dataout)
