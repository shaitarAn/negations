# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"

# python3 duplicate_sents_ES.py

# import xml.etree.ElementTree as ET
from lxml import etree
from pathlib import Path

outpath = Path('output/')
outpath.mkdir(parents=True, exist_ok=True)

article = format('test.xml')
# article = format(
# '/Users/anastassiashaitarova/Documents/thinkMASTER/datasets/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')

tree = etree.parse(article)


def parse_neg_structure(element, negs, i):

    tokens = []
    cues = []
    scope = []

    for el_in_neg_structure in list(element):

        if el_in_neg_structure.tag == 'scope':
            for el_in_scope in list(el_in_neg_structure):

                # if cue is a multiword it has attribute 'discid="1n/c"'
                if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                    for neg in el_in_scope.iter():
                        try:
                            if neg.get('wd'):
                                # print(neg.get('wd'))
                                tokens.append(neg.get('wd').upper())
                                cues.append(2)
                                scope.append(0)
                        except:
                            pass

                # regular cue has no attribute
                elif el_in_scope.tag == 'negexp':
                    for neg in el_in_scope.iter():
                        try:
                            if neg.get('wd'):
                                # print(neg.get('wd'))
                                tokens.append(neg.get('wd').upper())
                                cues.append(1)
                                scope.append(0)
                        except:
                            pass

                elif el_in_scope.tag == 'neg_structure':
                    negs += 1
                    print('NESTED', negs)
                    if negs == i:
                        toks, cus, scp, negs, i = parse_neg_structure(el_in_scope, negs, i)
                        tokens += toks
                        cues += cus
                        scope += scp
                        # i += 1

                else:
                    for neg in el_in_scope.iter():
                        try:
                            if neg.get('wd'):
                                # print(neg.get('wd'))
                                tokens.append(neg.get('wd'))
                                cues.append(3)
                                scope.append(1)
                        except:
                            pass

        elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
            for neg in el_in_neg_structure.iter():
                try:
                    if neg.get('wd'):
                        # print(neg.get('wd'))
                        tokens.append(neg.get('wd').upper())
                        cues.append(2)
                        scope.append(0)
                except:
                    pass

        # regular cue has no attribute
        elif el_in_neg_structure.tag == 'negexp':
            for neg in el_in_neg_structure.iter():
                try:
                    if neg.get('wd'):
                        # print(neg.get('wd'))
                        tokens.append(neg.get('wd').upper())
                        cues.append(1)
                        scope.append(0)
                except:
                    pass

        else:
            for el in el_in_neg_structure.iter():
                try:
                    if el.get('wd'):
                        tokens.append(el.get('wd'))
                        cues.append(3)
                        scope.append(0)
                except:
                    pass
    print('END OF LOOP', negs)

    return (tokens, cues, scope, negs, i)


def process_sentence(sentence, i, negs=0):

    tokens = []
    cues = []
    scope = []

    # negs = 0

    try:
        for element in sentence:

            # top level neg_structures
            if element.tag == 'neg_structure':
                negs += 1
                if negs == i:
                    print('first mention', negs)
                    toks, cus, scp, negs, i = parse_neg_structure(element, negs, i)
                    tokens += toks
                    cues += cus
                    scope += scp
                    print('insent', negs)

                else:
                    for el_in_neg_structure in element.iter():
                        try:
                            if el_in_neg_structure.get('wd'):
                                tokens.append(el_in_neg_structure.get('wd'))
                                cues.append(3)
                                scope.append(0)
                        except:
                            pass

                # print(negs)

            # collect other words in the sentence
            elif element.get('wd'):
                tokens.append(element.get('wd'))
                cues.append(3)
                scope.append(0)

    except TypeError:
        pass

    return (tokens, cues, scope)


for sentence in tree.findall('.//sentence'):
    elems = sentence.xpath('//negexp')
    negation_events = sum(1 for x in sentence.iter('neg_structure'))
    reslist = list(sentence.iter())
    text_tokens = [x.get('wd') for x in reslist if x.get('wd')]
    text = ' '.join([x.get('wd') for x in reslist if x.get('wd')])

    if negation_events > 0:
        print('negation_events: ', negation_events)
        for i in range(negation_events):
            tokens, cues, scope = process_sentence(sentence, i + 1, negs=0)
            print(len(tokens), len(text_tokens), ' '.join(tokens))
            print(cues)
            print(scope)
            print()

    print('***************************')
