# !/usr/bin/env python3
# -*- coding: utf8 -*-

from pathlib import Path
import json
import re
import html

'''
Extracts tokens and annotations from the original corpus,
creates a json file that is suitable for NegBERT.
'''

data1 = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_bioscope/full_papers.xml'
data2 = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/abstracts.xml'
data = [data1, data2]

TASK = 'negation'


def bioscope(f_path):

    file = open(f_path, encoding='utf-8')
    sentences = []
    for s in file:
        sentences += re.split("(<.*?>)", html.unescape(s))
    cue_sentence = []
    cue_cues = []
    cue_only_data = []
    scope_cues = []
    scope_scopes = []
    scope_sentence = []
    sentence = []
    cue = {}
    scope = {}
    in_scope = []
    in_cue = []
    word_num = 0
    c_idx = []
    s_idx = []
    in_sentence = 0
    for token in sentences:
        if token == '':
            continue
        elif '<sentence' in token:
            in_sentence = 1
        elif '<cue' in token:
            if TASK in token:
                # print(token)
                # print(str(re.split('(ref=".*?")', token)[1][4:]))
                in_cue.append(str(re.split('(ref=".*?")', token)[1][4:]))
                c_idx.append(str(re.split('(ref=".*?")', token)[1][4:]))
                cue[c_idx[-1]] = []
        elif '</cue' in token:
            in_cue = in_cue[:-1]
        elif '<xcope' in token:
            # print('token', token)
            # print(re.split('(id=".*?")', token)[1])
            in_scope.append(str(re.split('(id=".*?")', token)[1][3:]))
            s_idx.append(str(re.split('(id=".*?")', token)[1][3:]))
            scope[s_idx[-1]] = []
        elif '</xcope' in token:
            in_scope = in_scope[:-1]
        elif '</sentence' in token:
            # print(cue, scope)
            if len(cue.keys()) == 0:
                cue_only_data.append([sentence, [3] * len(sentence)])
            else:
                cue_sentence.append(sentence)
                cue_cues.append([3] * len(sentence))
                for i in cue.keys():
                    scope_sentence.append(sentence)
                    scope_cues.append([3] * len(sentence))
                    if len(cue[i]) == 1:
                        cue_cues[-1][cue[i][0]] = 1
                        scope_cues[-1][cue[i][0]] = 1
                    else:
                        for c in cue[i]:
                            cue_cues[-1][c] = 2
                            scope_cues[-1][c] = 2
                    scope_scopes.append([0] * len(sentence))

                    if i in scope.keys():
                        for s in scope[i]:
                            scope_scopes[-1][s] = 1

            sentence = []
            cue = {}
            scope = {}
            in_scope = []
            in_cue = []
            word_num = 0
            in_sentence = 0
            c_idx = []
            s_idx = []
        elif '<' not in token:
            if in_sentence == 1:
                words = token.split()
                sentence += words
                if len(in_cue) != 0:
                    for i in in_cue:
                        cue[i] += [word_num + i for i in range(len(words))]
                elif len(in_scope) != 0:
                    for i in in_scope:
                        scope[i] += [word_num + i for i in range(len(words))]
                word_num += len(words)

    return scope_sentence, scope_cues, scope_scopes


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('BIOSCOPE_2labels.json')
    textfile1 = outpath / Path('BIOSCOPE_sents.txt')
    textfile2 = outpath / Path('BIOSCOPE_2labels_anno.txt')

    json_data = [item[:3] for item in data]

    with open(outfile1, 'w') as outf1:
        json.dump(json_data, outf1)

    with open(textfile1, 'w', encoding='utf8') as outf:
        for item in data:
            print(item)
            outf.write(' '.join(item[0]) + '\n')

    count = 0
    with open(textfile2, 'w', encoding='utf8') as outf:
        for item in data:
            # print(item)
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

    sents, cues, scopes = bioscope(file)
    scope_sents.extend(sents)
    scope_cues.extend(cues)
    data_scope.extend(scopes)
    # print(len(sents), file)
    if 'full_papers' in file:
        # print(file)
        files.extend(['full_papers'] * len(sents))
    if 'abstracts' in file:
        files.extend(['abstracts'] * len(sents))

zipped_data = list(zip(scope_sents, scope_cues, data_scope, files))

write_files(zipped_data)
