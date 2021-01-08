# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"


from lxml import etree
from pathlib import Path
import os
import json


class SentenceParser():

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = []
        self.cues = []
        self.scope = []

    def parse_neg_structure(self, neg_structure):

        for el_in_neg_structure in list(neg_structure):

            if el_in_neg_structure.tag == 'scope':
                for el_in_scope in list(el_in_neg_structure):

                    # if cue is a multiword it has attribute 'discid="1n/c"'
                    if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                        for neg in el_in_scope.iter():
                            if neg.get('wd'):
                                self.split_tokens(neg, 2, 0, up=False)

                    # regular cue has no attribute
                    elif el_in_scope.tag == 'negexp':
                        for neg in el_in_scope.iter():
                            if neg.get('wd'):
                                if len(neg.get('wd').split('_')) > 1:
                                    self.split_tokens(neg, 2, 0, up=False)
                                else:
                                    self.split_tokens(neg, 1, 0, up=False)

                    elif el_in_scope.tag == 'event':
                        for n in el_in_scope:
                            if n.tag == 'negexp':
                                for el in n:
                                    if el.get('wd'):
                                        print(el.get('wd'))
                                        if len(el.get('wd').split('_')) > 1:
                                            self.split_tokens(el, 2, 0, up=False)
                                        else:
                                            self.split_tokens(el, 1, 0, up=False)

                            elif n.tag == 'scope':
                                for elem in n:
                                    if elem.tag == 'negexp':
                                        for el in elem:
                                            if el.get('wd'):
                                                # print(el.get('wd'))
                                                if len(el.get('wd').split('_')) > 1:
                                                    self.split_tokens(el, 2, 0, up=False)
                                                else:
                                                    self.split_tokens(el, 1, 0, up=False)
                                    elif elem.get('wd'):
                                        self.split_tokens(elem, 3, 1, up=False)

                            elif n.get('wd'):
                                self.split_tokens(n, 3, 1, up=False)

                    elif el_in_scope.get('wd'):
                        self.split_tokens(el_in_scope, 3, 1)

            elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
                for neg in el_in_neg_structure.iter():
                    if neg.get('wd'):
                        self.split_tokens(neg, 2, 0, up=False)

            # regular cue has no attribute
            elif el_in_neg_structure.tag == 'negexp':
                for neg in el_in_neg_structure.iter():
                    if neg.get('wd'):
                        if len(neg.get('wd').split('_')) > 1:
                            self.split_tokens(neg, 2, 0, up=False)
                        else:
                            self.split_tokens(neg, 1, 0, up=False)

            else:
                for el in el_in_neg_structure.iter():
                    if el.get('wd'):
                        self.split_tokens(el, 3, 0)

    def split_tokens(self, node, cue, scope, up=False):
        for token in node.get('wd').split('_'):
            if up:
                self.tokens.append(token.upper())
            else:
                self.tokens.append(token)
            self.cues.append(cue)
            self.scope.append(scope)


def get_path(elem):
    # inspired by https://stackoverflow.com/questions/39112938/parse-hierarchical-xml-tags
    path = []
    parent = elem.getparent()
    path.append(parent)
    while parent is not None:
        parent = parent.getparent()
        if parent is not None:
            path.append(parent)

    return path


def iter_sentences(infile):

    # breakpoint()

    tree = etree.parse(infile)

    for sentence in tree.findall('.//sentence'):

        negs_all = [elem for elem in sentence.iter() if elem.tag == "neg_structure"]

        if len(negs_all) > 0:

            for neg in negs_all:
                sent = SentenceParser(sentence)
                for elem in sentence.iter():
                    if elem == neg:
                        sent.parse_neg_structure(neg)
                    else:
                        if elem.get('wd'):
                            if neg not in get_path(elem):
                                sent.split_tokens(elem, 3, 0)

                yield sent.tokens, sent.cues, sent.scope


def write_files(data):

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('spanishALLdata.json')
    textfile1 = outpath / Path('spanishALLsents.txt')
    textfile2 = outpath / Path('spanishALLsents_anno.txt')

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

    # article = format('test.xml')
    article = '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/hoteles/no_1_7.tbf.xml'
    # article = format(
    # '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/')

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
