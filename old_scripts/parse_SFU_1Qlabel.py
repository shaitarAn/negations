# !/usr/bin/env python3
# -*- coding: utf8 -*-

import xml.etree.ElementTree as ET
import os
from pathlib import Path
import json


def clean_sent(word):
    newword = ''
    if not word.isascii():
        for w in word:
            if not w.isascii():
                newword += "'"
            else:
                newword += w
        word = newword
    return word


def iter_sentences(review):

    # breakpoint()

    tree = ET.parse(review)
    root = tree.getroot()

    for sentence in root.iter('SENTENCE'):
        cues = []
        scope = []
        negation_events = sum(1 for elem in sentence.iter('cue') if elem.tag ==
                              'cue' and elem.attrib['type'] == 'negation')
        sent = [clean_sent(t.text) for t in sentence.iter('W')]
        cue_ID = ''

        if negation_events <= 1:
            for element in list(sentence):
                for item in element.iter():
                    if item.tag == 'cue' and item.attrib['type'] == 'negation':
                        cue_words = [w.text for w in list(item) if w.tag == 'W']
                        cue_ID = item.attrib['ID']
                        for word in item.findall('W'):
                            # print(word.text)
                            if len(cue_words) == 1:
                                cues.append(1)
                                scope.append(0)
                            elif len(cue_words) > 1:
                                cues.append(1)
                                scope.append(0)
                            else:
                                pass

                    elif item.tag == 'cue' and item.attrib['type'] != 'negation':
                        for word in item.findall('W'):
                            cues.append(3)
                            scope.append(0)

                    elif item.tag == 'xcope':
                        ID = False
                        for e in list(item):
                            if e.tag == 'ref':
                                if cue_ID == e.attrib['SRC']:
                                    ID = True
                            if ID is True:
                                if e.tag == 'W':
                                    cues.append(3)
                                    scope.append(1)
                            else:
                                if e.tag == 'W':
                                    cues.append(3)
                                    scope.append(0)

                if element.tag == 'W':
                    cues.append(3)
                    scope.append(0)

        else:
            negations = sum(1 for elem in sentence if elem.tag == 'xcope')
            if negations == 1:
                for element in list(sentence):
                    for item in element.iter():
                        if item.tag == 'cue' and item.attrib['type'] == 'negation':
                            pass

            elif negations > 1:
                print('WOW')

        yield sent, scope, cues


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('SFU_1label_noNONEG.json')
    textfile1 = outpath / Path('SFU_noNONEG.txt')
    textfile2 = outpath / Path('SFU_1label_noNONEG_anno.txt')

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


def main():

    all_sentences = []
    all_cues = []
    all_scopes = []
    all_files = []

    # for multiple neg events
    article = "/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_SFU_Review_Corpus_Negation_Speculation/MUSIC/no11done.xml"

    # nested 'neither nor' cue
    # /Users/anastassiashaitarova/Documents/thinkMASTER/datasets/en_SFU_Review_Corpus_Negation_Speculation/CARS/no10done.xml

    if os.path.isdir(article):

        for dir_name in os.listdir(article):
            if '.' not in dir_name:
                for f_name in os.listdir(article + "/" + dir_name):
                    my_file_name = article + '/' + dir_name + '/' + f_name
                    file_name = dir_name + '/' + f_name

                    all_sentences.extend([sent[0] for sent in iter_sentences(my_file_name)])
                    all_cues.extend([sent[1] for sent in iter_sentences(my_file_name)])
                    all_scopes.extend([sent[2] for sent in iter_sentences(my_file_name)])
                    all_files.extend([file_name for item in iter_sentences(my_file_name)])

        data = list(zip(all_sentences, all_cues, all_scopes, all_files))

        write_files(data)

    else:

        # breakpoint()

        all_sentences.extend([sent[0] for sent in iter_sentences(article)])
        all_cues.extend([sent[1] for sent in iter_sentences(article)])
        all_scopes.extend([sent[2] for sent in iter_sentences(article)])

        data = list(zip(all_sentences, all_cues, all_scopes))

        for item in data:
            print(item[0])
            print(item[1])
            print(item[2])
            print()


if __name__ == '__main__':
    main()
