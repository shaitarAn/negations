# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"


from lxml import etree
from pathlib import Path
import os
# import json


class SentenceParser():

    def __init__(self, sentence, i):
        self.sentence = sentence
        self.turn = i
        self.negs = 0
        self.tokens = []
        self.cues = []
        self.scope = []

    def parse_neg_structure(self, neg_structure):

        self.negs += 1
        if self.negs == self.turn:

            for el_in_neg_structure in list(neg_structure):

                if el_in_neg_structure.tag == 'scope':
                    for el_in_scope in list(el_in_neg_structure):

                        # if cue is a multiword it has attribute 'discid="1n/c"'
                        if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                            for neg in el_in_scope.iter():
                                if neg.get('wd'):
                                    self.split_tokens(neg, 2, 0, up=True)

                        # regular cue has no attribute
                        elif el_in_scope.tag == 'negexp':
                            for neg in el_in_scope.iter():
                                if neg.get('wd'):
                                    if len(neg.get('wd').split('_')) > 1:
                                        self.split_tokens(neg, 2, 0, up=True)
                                    else:
                                        self.split_tokens(neg, 1, 0, up=True)

                        else:
                            for neg in el_in_scope.iter():
                                if neg.get('wd'):
                                    self.split_tokens(neg, 3, 1)

                elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
                    for neg in el_in_neg_structure.iter():
                        if neg.get('wd'):
                            self.split_tokens(neg, 2, 0, up=True)

                # regular cue has no attribute
                elif el_in_neg_structure.tag == 'negexp':
                    for neg in el_in_neg_structure.iter():
                        if neg.get('wd'):
                            if len(neg.get('wd').split('_')) > 1:
                                self.split_tokens(neg, 2, 0, up=True)
                            else:
                                self.split_tokens(neg, 1, 0, up=True)

                else:
                    for el in el_in_neg_structure.iter():
                        if el.get('wd'):
                            self.split_tokens(el, 3, 0)

        else:
            for el_in_neg_structure in neg_structure.iter():
                if el_in_neg_structure.get('wd'):
                    self.split_tokens(el_in_neg_structure, 3, 0)

    def process_sentence(self):

        try:
            for element in self.sentence:

                # top level neg_structures
                if element.tag == 'neg_structure':
                    self.parse_neg_structure(element)

                elif element.get('wd'):
                    self.split_tokens(element, 3, 0)

        except TypeError:
            pass

    def split_tokens(self, node, cue, scope, up=False):
        for token in node.get('wd').split('_'):
            if up:
                self.tokens.append(token.upper())
            else:
                self.tokens.append(token)
            self.cues.append(cue)
            self.scope.append(scope)


def get_depth(elem):
    # from https://stackoverflow.com/questions/39112938/parse-hierarchical-xml-tags
    path = []
    # if elem.get('wd'):
    #     path.append(elem.get('wd'))
    parent = elem.getparent()
    # print(elem.tag, parent.tag)
    path.append(parent)
    while parent is not None:
        parent = parent.getparent()
        if parent is not None:
            path.append(parent)

    return path


def iter_sentences(infile):

    tree = etree.parse(infile)
    leve1_negation_events = 0
    all_negs = 0
    all_sents = []

    for sentence in tree.findall('.//sentence'):

        negs_1level = [x for x in sentence.findall('neg_structure')]

        negs_all = [elem for elem in sentence.iter() if elem.tag == "neg_structure"]

        leve1_negation_events += len(negs_1level)
        all_negs += len(negs_all)

        reslist = list(sentence.iter())
        text_tokens = [x.get('wd') for x in reslist if x.get('wd')]

        negs_nested = [elem for elem in negs_all if elem not in negs_1level]

        if len(negs_1level) > 0:
            print('neg_events top level: ', len(negs_1level))
            print('neg_events all:', len(negs_all))
            for i in range(len(negs_1level)):
                sent = SentenceParser(sentence, i + 1)
                sent.process_sentence()
                all_sents.append(sent.tokens)
                print(len(sent.tokens), len(text_tokens), ' '.join(sent.tokens))
                print(sent.cues)
                print(sent.scope)
                print()

            if len(negs_1level) != len(negs_all):
                for neg in negs_nested:
                    sent_nested = SentenceParser(sentence, 1)
                    for elem in sentence.iter():
                        if elem == neg:
                            sent_nested.parse_neg_structure(neg)
                        else:
                            if elem.get('wd'):
                                if neg not in get_depth(elem):
                                    sent_nested.split_tokens(elem, 3, 0)

                    all_sents.append(sent_nested.tokens)
                    print()
                    print(len(sent_nested.tokens), ' '.join(sent_nested.tokens))
                    print(sent_nested.cues)
                    print(sent_nested.scope)
                    print()

            print('***************************')

    return leve1_negation_events, all_negs, all_sents


def main():

    negs1 = 0
    negsall = 0
    all_sentences = []
    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    # article = format('test.xml')
    # article = format(
    # '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')
    article = format(
        '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/')

    if os.path.isdir(article):

        for dir_name in os.listdir(article):
            if '.' not in dir_name:
                for f_name in os.listdir(article + "/" + dir_name):
                    my_file_name = article + '/' + dir_name + '/' + f_name
                    # file_name = dir_name + '/' + f_name

                    negation_events, all_negs, all_sents = iter_sentences(my_file_name)
                    negs1 += negation_events
                    negsall += all_negs
                    all_sentences.extend(all_sents)

    else:
        negation_events, all_negs, all_sents = iter_sentences(article)
        negs1 += negation_events
        negsall += all_negs
        all_sentences.extend(all_sents)

    print('total leve1_negation_events', '\t', negs1)
    print('All neg structures', negsall)
    print(len(all_sentences))


if __name__ == '__main__':
    main()
