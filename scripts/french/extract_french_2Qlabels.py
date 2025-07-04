# !/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Uses starsem() function from NegBERT.
Converts French data into token, cue, scope vectors.
Randomly splits data into 100 sentence training set and XX set.
Writes three json files into /output directory.
'''

__author__ = "Anastassia Shaitarova"

# python3 extract_and_split_french.py
import random
from collections import defaultdict
from pathlib import Path
import json

data1 = "../corpora/CAS_sherlock_full.txt"
data2 = "../corpora/ESSAI_sherlock_full.txt"

data = [data1, data2]


def starsem(f_path):
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


def sample(iterable, k):
    training = []
    rest = []
    for t, item in enumerate(iterable):
        if t < k:
            training.append(item)
        else:
            m = random.randint(0, t)
            if m < k:
                item, training[m] = training[m], item
            rest.append(item)

    return training, rest


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('FRENCH_2labels.json')
    textfile1 = outpath / Path('FRENCH_sents.txt')
    textfile2 = outpath / Path('FRENCH_2labels_anno.txt')

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
    if 'CAS' in file:
        # print(file)
        files.extend(['CAS'] * len(sents))
    if 'ESSAI' in file:
        files.extend(['ESSAI'] * len(sents))

zipped_data = []
zipped_data2 = list(zip(scope_sents, scope_cues, data_scope, files))
for item in zipped_data2:
    if item not in zipped_data:
        zipped_data.append(item)

write_files(zipped_data)

#
print(len(zipped_data))
