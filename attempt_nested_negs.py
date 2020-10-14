# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"


# import xml.etree.ElementTree as ET
from lxml import etree
from pathlib import Path


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
                                try:
                                    if neg.get('wd'):
                                        # print(neg.get('wd'))
                                        self.tokens.append(neg.get('wd').upper())
                                        self.cues.append(2)
                                        self.scope.append(0)
                                except:
                                    pass

                        # regular cue has no attribute
                        elif el_in_scope.tag == 'negexp':
                            for neg in el_in_scope.iter():
                                try:
                                    if neg.get('wd'):
                                        # print('I AM HERE', neg.get('wd'))
                                        self.tokens.append(neg.get('wd').upper())
                                        self.cues.append(1)
                                        self.scope.append(0)
                                except:
                                    pass

                        elif el_in_scope.tag == 'neg_structure':
                            self.negs += 1
                            self.turn += 1
                            print('NESTED', self.negs, self.turn)
                            if self.negs == self.turn:
                                print('GO TO NESTED')
                                self.parse_neg_structure(el_in_scope)
                                # nested = SentenceParser.parse_neg_structure(el_in_scope)
                                # self.negs = nested.negs
                                # self.turn = nested.turn

                        else:
                            for neg in el_in_scope.iter():
                                try:
                                    if neg.get('wd'):
                                        # print(neg.get('wd'))
                                        self.tokens.append(neg.get('wd'))
                                        self.cues.append(3)
                                        self.scope.append(1)
                                except:
                                    pass

                elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
                    for neg in el_in_neg_structure.iter():
                        try:
                            if neg.get('wd'):
                                # print(neg.get('wd'))
                                self.tokens.append(neg.get('wd').upper())
                                self.cues.append(2)
                                self.scope.append(0)
                        except:
                            pass

                # regular cue has no attribute
                elif el_in_neg_structure.tag == 'negexp':
                    for neg in el_in_neg_structure.iter():
                        try:
                            if neg.get('wd'):
                                # print(neg.get('wd'))
                                self.tokens.append(neg.get('wd').upper())
                                self.cues.append(1)
                                self.scope.append(0)
                        except:
                            pass

                else:
                    for el in el_in_neg_structure.iter():
                        try:
                            if el.get('wd'):
                                self.tokens.append(el.get('wd'))
                                self.cues.append(3)
                                self.scope.append(0)
                        except:
                            pass

        else:
            for el_in_neg_structure in neg_structure.iter():
                try:
                    if el_in_neg_structure.get('wd'):
                        self.tokens.append(el_in_neg_structure.get('wd'))
                        self.cues.append(3)
                        self.scope.append(0)
                except:
                    pass

    def process_sentence(self):

        try:
            for element in self.sentence:

                # top level neg_structures
                if element.tag == 'neg_structure':
                    self.parse_neg_structure(element)

                elif element.get('wd'):
                    self.tokens.append(element.get('wd'))
                    self.cues.append(3)
                    self.scope.append(0)

        except TypeError:
            pass


def iter_sentences(infile):

    tree = etree.parse(infile)

    for sentence in tree.findall('.//sentence'):
        negation_events = sum(1 for x in sentence.iter('neg_structure'))
        reslist = list(sentence.iter())
        text_tokens = [x.get('wd') for x in reslist if x.get('wd')]
        text = ' '.join([x.get('wd') for x in reslist if x.get('wd')])

        if negation_events > 0:
            print('negation_events: ', negation_events)
            for i in range(negation_events):
                sent = SentenceParser(sentence, i + 1)
                sent.process_sentence()
                print(len(sent.tokens), len(text_tokens), ' '.join(sent.tokens))
                print(sent.cues)
                print(sent.scope)
                print()

        print('***************************')


def main():

    outpath = Path('output/')
    outpath.mkdir(parents=True, exist_ok=True)

    article = format('test.xml')
    # article = format(
    # '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')

    iter_sentences(article)


if __name__ == '__main__':
    main()
