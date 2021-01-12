import re
import os
import html
import json
# import random
from pathlib import Path

sfu_data = "/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_SFU_Review_Corpus_Negation_Speculation/"
TASK = "negation"


def clean_sent(word):
    newword = ''
    if not word.isascii() and len(word) > 1:
        for w in word:
            if not w.isascii():
                # print(w, len(word))
                newword += "'"
            else:
                # print('newword', newword)
                newword += w
        word = newword
    elif not word.isascii():
        word = 'ABRACADABRA'
    return word


def sfu_review(f_path):
    # print(f_path)
    file = open(f_path, encoding='utf-8')
    sentences = []
    for s in file:
        sentences += re.split("(<.*?>)", html.unescape(s))
    # print(sentences)
    cue_sentence = []
    cue_cues = []
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
    cue_only_data = []
    s_idx = []
    in_word = 0
    for token in sentences:
        # print(token)
        if token == '':
            continue
        elif token == '<W>':
            in_word = 1
        elif token == '</W>':
            in_word = 0
            word_num += 1
        elif '<cue' in token:
            if TASK in token:
                in_cue.append(int(re.split('(ID=".*?")', token)[1][4:-1]))
                c_idx.append(int(re.split('(ID=".*?")', token)[1][4:-1]))
                cue[c_idx[-1]] = []
        elif '</cue' in token:
            in_cue = in_cue[:-1]
        elif '<xcope' in token:
            continue
        elif '</xcope' in token:
            in_scope = in_scope[:-1]
        elif '<ref' in token:
            in_scope.append([int(i) for i in re.split('(SRC=".*?")', token)[1][5:-1].split(' ')])
            s_idx.append([int(i) for i in re.split('(SRC=".*?")', token)[1][5:-1].split(' ')])
            for i in s_idx[-1]:
                scope[i] = []
        elif '</SENTENCE' in token:
            if len(cue.keys()) == 0:
                cue_only_data.append([sentence, [3] * len(sentence)])
            else:
                cue_sentence.append(sentence)
                cue_cues.append([3] * len(sentence))
                for i in cue.keys():
                    # print(sentence)
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
            in_word = 0
            c_idx = []
            s_idx = []
        elif '<' not in token:
            if in_word == 1:
                if len(in_cue) != 0:
                    for i in in_cue:
                        cue[i].append(word_num)
                if len(in_scope) != 0:
                    for i in in_scope:
                        for j in i:
                            scope[j].append(word_num)

                sentence.append(clean_sent(token))

    return scope_sentence, scope_cues, scope_scopes


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('SFU_2label.json')
    textfile1 = outpath / Path('SFU_sents.txt')
    textfile2 = outpath / Path('SFU_2label_anno.txt')

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
        newzippy = [i for i in zippy if i[0] not in ["ABRACADABRA", "~"]]

        # reconstruct the data for json
        newlist = []
        for i in zip(*newzippy):
            newlist.append(list(i))
        newlist.append(item[3])
        # print(newlist)

        dataout.append(newlist)

    return dataout


sfu_tokens = []
sfu_cues = []
sfu_scopes = []
file_names = []

for dir_name in os.listdir(sfu_data):
    if '.' not in dir_name:
        for f_name in os.listdir(sfu_data + "//" + dir_name):
            sents, cues, scopes = sfu_review(sfu_data + "//" + dir_name + '//' + f_name)
            sfu_tokens.extend(sents)
            sfu_cues.extend(cues)
            sfu_scopes.extend(scopes)
            file_names.append(f_name)

all_data = zip(sfu_tokens, sfu_cues, sfu_scopes, file_names)

# for item in all_data:
#     print(item)

all_data = postprocess(all_data)

for item in all_data:
    print(item[0])
    print(item[1])
    print(item[2])
    print(item[3])

write_files(all_data)
