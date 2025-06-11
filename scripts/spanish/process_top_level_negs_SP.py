# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"

# python3 duplicate_sents_ES.py

# import xml.etree.ElementTree as ET
from lxml import etree
from pathlib import Path
import os

outpath = Path('output/')
outpath.mkdir(parents=True, exist_ok=True)

article = format('/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/')

all_neg_sents = 0
new_sents = 0
all_neg_structures = 0
nested_neg_sents = 0
lost = 0


def process_sentence(sentence, i, negation_events):

    tokens = []
    cues = []
    scope = []

    negs = 0

    try:
        for element in sentence:

            # top level neg_structures
            if element.tag == 'neg_structure':
                negs += 1
                if negs == i:

                    for el_in_neg_structure in list(element):

                        if el_in_neg_structure.tag == 'scope':
                            for el_in_scope in list(el_in_neg_structure):

                                # if cue is a multiword it has attribute 'discid="1n/c"'
                                if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                                    for neg in el_in_scope.iter():
                                        try:
                                            if neg.get('wd'):
                                                for token in neg.get('wd').split('_'):
                                                    tokens.append(token.upper())
                                                    cues.append(2)
                                                    scope.append(0)
                                        except:
                                            pass

                                # regular cue has no attribute
                                elif el_in_scope.tag == 'negexp':
                                    for neg in el_in_scope.iter():
                                        try:
                                            if neg.get('wd'):
                                                for token in neg.get('wd').split('_'):
                                                    tokens.append(token.upper())
                                                    cues.append(1)
                                                    scope.append(0)
                                        except:
                                            pass

                                else:
                                    for neg in el_in_scope.iter():
                                        try:
                                            if neg.get('wd'):
                                                for token in neg.get('wd').split('_'):
                                                    tokens.append(token)
                                                    cues.append(3)
                                                    scope.append(1)
                                        except:
                                            pass

                        elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
                            for neg in el_in_neg_structure.iter():
                                try:
                                    if neg.get('wd'):
                                        for token in neg.get('wd').split('_'):
                                            tokens.append(token.upper())
                                            cues.append(2)
                                            scope.append(0)
                                except:
                                    pass

                        # regular cue has no attribute
                        elif el_in_neg_structure.tag == 'negexp':
                            for neg in el_in_neg_structure.iter():
                                try:
                                    if neg.get('wd'):
                                        for token in neg.get('wd').split('_'):
                                            tokens.append(token.upper())
                                            cues.append(1)
                                            scope.append(0)
                                except:
                                    pass

                        else:
                            for el in el_in_neg_structure.iter():
                                try:
                                    if el.get('wd'):
                                        for token in el.get('wd').split('_'):
                                            tokens.append(token)
                                            cues.append(3)
                                            scope.append(0)
                                except:
                                    pass

                else:
                    for el_in_neg_structure in element.iter():
                        try:
                            if el_in_neg_structure.get('wd'):
                                for token in el_in_neg_structure.get('wd').split('_'):
                                    tokens.append(token)
                                    cues.append(3)
                                    scope.append(0)
                        except:
                            pass

            # collect other words in the sentence
            elif element.get('wd'):
                for token in element.get('wd').split('_'):
                    tokens.append(token)
                    cues.append(3)
                    scope.append(0)

    except TypeError:
        pass

    return (tokens, cues, scope)


for dir_name in os.listdir(article):

    if '.' not in dir_name:
        for f_name in os.listdir(article + "/" + dir_name):
            my_file_name = article + '/' + dir_name + '/' + f_name
            file_name = dir_name + '/' + f_name

            tree = etree.parse(my_file_name)

            for sentence in tree.findall('.//sentence'):
                elems = sentence.xpath('//negexp')
                # find top level neg_structures
                negation_events = sum(1 for x in sentence.findall('neg_structure'))
                # find all neg_structures in the sentence
                all_negation_events = sum(1 for x in sentence.iter('neg_structure'))

                if negation_events != all_negation_events:
                    print('HIDDEN NEG_STRUCTURES')
                    nested_neg_sents += 1

                if negation_events > 0:
                    all_neg_sents += 1

                lost += abs(negation_events - all_negation_events)

                new_sents += negation_events
                all_neg_structures += all_negation_events

                reslist = list(sentence.iter())
                text_tokens = [x.get('wd') for x in reslist if x.get('wd')]
                text = ' '.join([x.get('wd') for x in reslist if x.get('wd')])

                if negation_events > 0:
                    print(file_name)
                    print('negation_events: ', negation_events)
                    for i in range(negation_events):
                        tokens, cues, scope = process_sentence(sentence, i + 1, negation_events)
                        print(len(tokens), len(text_tokens), ' '.join(tokens))
                        print(cues)
                        print(scope)
                        print()

                print('***************************')

print('all_neg_sents', '\t' * 2, all_neg_sents)
print('newly collected sents', '\t', new_sents)
print('all_neg_structures', '\t', all_neg_structures)
print('nested_neg_sents', '\t', all_neg_structures)
print('I lost {} negstructures'.format(lost))
