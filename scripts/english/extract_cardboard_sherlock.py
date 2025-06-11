# !/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Extracts tokens and annotations from the original corpus,
removes odd quotation marks, creates a json file that is suitable for NegBERT.
'''

from collections import defaultdict
from pathlib import Path
import json

data = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_Sherlock_dataset/cd-sco/corpus/test-gold/SEM-2012-SharedTask-CD-SCO-test-cardboard-GOLD.txt'


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

    starsem_scopes = (scope_sents, scope_cues, data_scope)
    return starsem_scopes


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('SHERLOCK_cardbord.json')

    with open(outfile1, 'w') as outf1:
        json.dump(data, outf1)


starsem_scopes = starsem(data)
scope_sents, scope_cues, data_scope = starsem_scopes
zipped_data = list(zip(scope_sents, scope_cues, data_scope))

newzippy = []
dataout = []
for item in zipped_data:
    zippy = zip(item[0], item[1], item[2])

    # remove unconventional quotation marks
    newzippy = [i for i in zippy if i[0] not in ['``', "'", "''", "`"]]

    # reconstruct the data for json
    newlist = tuple()
    for item in zip(*newzippy):
        newlist = newlist + (list(item),)

    dataout.append(newlist)

write_files(dataout)
