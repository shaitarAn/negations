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

    # def parse_nested_structure(self, neg_structure):
    #
    #     sent = []
    #     for element in self.sentence:
    #         for neg in element.iter():
    #             if neg.get('wd'):
    #                 sent.append(neg.get('wd').upper())
    #
    #     print(len(sent), ' '.join(sent))
    #     print()


def get_depth(elem):
    # from https://stackoverflow.com/questions/39112938/parse-hierarchical-xml-tags
    parent = elem.getparent()
    # print(elem.tag, parent.tag)
    path = [parent.tag]
    while parent is not None:
        parent = parent.getparent()
        if parent is not None:
            path.append(parent.tag)

    return path


def iter_sentences(infile):

    tree = etree.parse(infile)
    collected_negation_events = 0

    for sentence in tree.findall('.//sentence'):

        negs_1level = [x for x in sentence.findall('neg_structure')]

        negs_all = [elem for elem in sentence.iter() if elem.tag == "neg_structure"]

        collected_negation_events += len(negs_1level)
        reslist = list(sentence.iter())
        text_tokens = [x.get('wd') for x in reslist if x.get('wd')]

        negs_nested = [elem for elem in negs_all if elem not in negs_1level]

        if len(negs_1level) > 0:
            print('neg_events top level: ', len(negs_1level))
            print('neg_events all:', len(negs_all))
            for i in range(len(negs_1level)):
                sent = SentenceParser(sentence, i + 1)
                sent.process_sentence()
                print(len(sent.tokens), len(text_tokens), ' '.join(sent.tokens))
                print(sent.cues)
                print(sent.scope)
                print()

            nested_sentence = []
            nested_cues = []
            nested_scope = []
            for neg in negs_nested:
                sent_nested = SentenceParser(sentence, 1)
                for elem in sentence.iter():
                    if elem == neg:
                        sent_nested.parse_neg_structure(neg)
                        nested_sentence.extend(sent_nested.tokens)
                        nested_cues.extend(sent_nested.cues)
                        nested_scope.extend(sent_nested.scope)
                    else:
                        if elem.get('wd'):
                            if sum(1 for x in get_depth(elem) if x == 'neg_structure') < 2:
                                nested_sentence.append(elem.get('wd'))
                                nested_cues.append(3)
                                nested_scope.append(0)
                                # print(elem.get('wd'), get_depth(elem))
            print(len(nested_sentence), nested_sentence)
            print(nested_cues)
            print(nested_scope)
            print('***************************')

    return collected_negation_events


def main():

    new_sents = 0
    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    article = format('test.xml')
    # article = format(
    # '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')
    # article = format(
    #     '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/')

    if os.path.isdir(article):

        for dir_name in os.listdir(article):
            if '.' not in dir_name:
                for f_name in os.listdir(article + "/" + dir_name):
                    my_file_name = article + '/' + dir_name + '/' + f_name
                    # file_name = dir_name + '/' + f_name

                    negation_events = iter_sentences(my_file_name)
                    new_sents += negation_events

    else:
        iter_sentences(article)

    print('newly collected sents', '\t', new_sents)


if __name__ == '__main__':
    main()
