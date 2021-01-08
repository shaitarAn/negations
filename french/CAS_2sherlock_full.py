# !/usr/bin/env python3
# -*- coding: utf8 -*-

'''
Converts the entire french CAS or ESSAI corpus into the format of SEM*12 corpus.
'''

__author__ = "Anastassia Shaitarova"

from collections import defaultdict
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_rows', None)

corpus = "ESSAI"

if corpus == "CAS":
    infile = "corpora/CAS_neg.txt"
    outfile = "corpora/CAS_sherlock_full.txt"
else:
    infile = "corpora/ESSAI_neg.txt"
    outfile = "corpora/ESSAI_sherlock_full.txt"

# original columns: sentence, token_id, word, lemma, POS, [optional: cue, scope]

# dictionary to group sentences by number
sents = defaultdict(list)

# fixed sentences
CAS = []


def move_cues(block):
    '''
    Splits multiple cues and scopes into different columns.
    '''
    scopes = 0
    cues = 0
    new_sent = []
    for line in block:
        # print(line)
        if len(line) > 6:
            line.append('_')
            if line[5].startswith('B'):
                cues += 1
                if cues == 1:
                    line[5] = line[2]
                elif cues == 2:
                    line.extend([line[2], '_', '_'])
                    line[5] = '_'
                elif cues == 3:
                    line.extend(['_', '_', '_', line[2], '_', '_'])
                    line[5] = '_'
                new_sent.append(line)
            elif line[5].startswith('I'):
                if cues == 1:
                    line[5] = line[2]
                elif cues == 2:
                    line.extend([line[2], '_', '_'])
                    line[5] = '_'
                elif cues == 3:
                    line.extend(['_', '_', '_', line[2], '_', '_'])
                    line[5] = '_'
                new_sent.append(line)
            elif line[6].startswith('B'):
                scopes += 1
                if scopes == 1:
                    line[6] = line[2]
                elif scopes == 2:
                    line.extend(['_', line[2], '_'])
                    line[6] = '_'
                elif scopes == 3:
                    line.extend(['_', '_', '_', '_', line[2], '_'])
                    line[6] = '_'
                new_sent.append(line)
            elif line[6].startswith('I'):
                if scopes == 1:
                    line[6] = line[2]
                elif scopes == 2:
                    line.extend(['_', line[2], '_'])
                    line[6] = '_'
                elif scopes == 3:
                    line.extend(['_', '_', '_', '_', line[2], '_'])
                    line[6] = '_'
                new_sent.append(line)
            else:
                new_sent.append(line)
        else:
            new_sent.append(line)

    return new_sent


with open(infile, 'r', encoding='utf8') as inf:
    for line in inf:
        line = line.strip().split('\t')
        # print(len(line))
        if len(line) > 1:
            # group sentences
            sentence = line[0]
            sents[sentence].append(line)
        else:
            pass

# process each sentence looking for multiple scopes
for s, sens in sents.items():
    ns = move_cues(sens)
    m = max([len(x) for x in ns])

    # pad sentences depending on the max length within the sentence
    for l in ns:
        line = l + ['_'] * (m - len(l))
        CAS.append(line)
    CAS.append([])

tempfile = "output/temp_cas_reformat.txt"

with open(tempfile, 'w', encoding='utf8') as out:
    for line in CAS:
        out.write('\t'.join(line))
        out.write('\n')

# ################

my_columns = ['sentence', 'token_id', 'word', 'lemma', 'POS',
              'cue1', 'scope1', 'event1', 'cue2', 'scope2', 'event2', 'cue3', 'scope3', 'event3']

df = pd.read_csv(tempfile, skip_blank_lines=False, header=None, sep="\t", names=my_columns)

# add columns
df.insert(0, "chapter", np.nan)
df.insert(6, "UDP", np.nan)

# add dummy string within sentences
df['chapter'].loc[df['word'].notnull()] = corpus.lower()
df['UDP'].loc[df['word'].notnull()] = 'dummy'
print(df.info())

# remove the last empty line in the file
df.drop(df.tail(1).index, inplace=True)

# write to file
df.to_csv(outfile, mode='w', sep="\t", header=None, index=False)

os.remove(tempfile)
