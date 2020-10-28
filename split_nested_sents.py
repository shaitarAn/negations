# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"


from lxml import etree
from pathlib import Path
import os
import json


class SentenceParser():

    def __init__(self, sentence, i):
        self.sentence = sentence
        self.dict_sentence = self.index_tokens(sentence)
        self.turn = i
        self.negs = 0
        self.tokens = []
        self.cues = []
        self.scope = []

    def index_tokens(self, sentence):

        sent = []
        my_dict = {}
        ind = 0
        for item in sentence.iter():
            if item.get('wd'):
                for token in item.get('wd').split('_'):
                    my_dict[ind] = token
                    ind += 1
                    sent.append(token)
        # print(my_dict)
        return my_dict

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


def get_depth(element):
    # from https://stackoverflow.com/questions/39112938/parse-hierarchical-xml-tags
    for elem in element:
        parent = elem.getparent()
        path = [parent.tag]
        while parent is not None:
            parent = parent.getparent()
            if parent is not None:
                path.append(parent.tag)

        if 'neg_structure' in path:
            return elem, path


def iter_sentences(infile):

    tree = etree.parse(infile)
    collected_negation_events = 0

    for sentence in tree.findall('.//sentence'):
        negation_events = sum(1 for x in sentence.findall('neg_structure'))
        collected_negation_events += negation_events
        reslist = list(sentence.iter())
        text_tokens = [x.get('wd') for x in reslist if x.get('wd')]

        if negation_events > 0:
            print('negation_events: ', negation_events)
            for i in range(negation_events):
                sent = SentenceParser(sentence, i + 1)
                sent.process_sentence()
                print(len(sent.tokens), len(text_tokens), ' '.join(sent.tokens))
                print(sent.cues)
                print(sent.scope)
                print()

            elems = sentence.xpath('.//neg_structure')
            elem, path = get_depth(elems)
            sent_nest = SentenceParser(sentence, 1)
            for element in sentence:

                if element.get('wd'):
                    # self.split_tokens(element, 3, 0)
                    sent_nest.tokens.append(element.get('wd'))
                    sent_nest.cues.append(3)
                    sent_nest.scope.append(0)

                else:
                    for negstr in sentence.iter():
                        if negstr == elem:
                            sent_nest.parse_neg_structure(elem)
                            print('YES')
                        if negstr.get('wd'):
                            # self.split_tokens(element, 3, 0)
                            sent_nest.tokens.append(negstr.get('wd'))
                            sent_nest.cues.append(3)
                            sent_nest.scope.append(0)

            print(sent_nest.tokens)
            print(sent_nest.cues)
            print(sent_nest.scope)

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
