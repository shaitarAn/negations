# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"

# python3 duplicate_sents_ES.py

# import xml.etree.ElementTree as ET
from lxml import etree
from pathlib import Path
import re

outpath = Path('output/')
outpath.mkdir(parents=True, exist_ok=True)

article = format('test.xml')

tree = etree.parse(article)

pattern = re.compile('neg_structure\\[(.)')


# counts the number of parents to the root element
def get_depth(element):
    # from https://stackoverflow.com/questions/39112938/parse-hierarchical-xml-tags
    depth = 0
    parent = element.getparent()
    path = [parent.tag]
    while parent is not None and not str(parent.tag).startswith('sentence'):
        # print(parent.tag)
        depth += 1
        parent = parent.getparent()
        if parent is not None:
            path.append(parent.tag)

    return path


def process_sentence(sentence, i, negation_events):
    negs = 0

    try:
        for element in sentence:

            # top level neg_structures
            if element.tag == 'neg_structure':
                negs += 1
                print('A', negs)
                for el_in_neg_structure in list(element):

                    if el_in_neg_structure.tag == 'scope':
                        # print('*** beginning of scope ***')
                        for el_in_scope in list(el_in_neg_structure):

                            # if cue is a multiword it has attribute 'discid="1n/c"'
                            if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                                for neg in list(el_in_scope):
                                    pass

                            # regular cue has no attribute
                            elif el_in_scope.tag == 'negexp':
                                for neg in list(el_in_scope):
                                    path = neg.getroottree().getpath(neg)
                                    paths = path.split('/')
                                    if pattern.search(path):
                                        ns = pattern.search(path).group(1)
                                    if negs == i:
                                        print(get_depth(neg)[::-1])
                                        print(negation_events)

                            elif el_in_scope.tag == 'neg_structure':
                                negs += 1
                                print('C', negs)
                                for neg in list(el_in_scope):
                                    if neg.tag == 'scope':
                                        for s in list(neg):
                                            if s.tag == 'negexp':
                                                for n in list(s):
                                                    if n.tag == 'event':
                                                        for e in list(n):
                                                            if negs == i:
                                                                # path = e.getroottree().getpath(e)
                                                                # paths = path.split('/')
                                                                # print(paths)
                                                                print(get_depth(e)[::-1])
                                                                print(negation_events)

                        # process nested neg_structure
                    elif el_in_neg_structure.tag == 'neg_structure':
                        negs += 1
                        print('B', negs, i)
                        for subsection in list(el_in_neg_structure):
                            if subsection.tag == 'scope':
                                for el_in_scope in list(subsection):

                                    # if cue is a multiword it has attribute 'discid="1n/c"'
                                    if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                                        for neg in list(el_in_scope):
                                            pass

                                    # regular cue has no attribute
                                    elif el_in_scope.tag == 'negexp':
                                        for neg in list(el_in_scope):
                                            if negs == i:
                                                # path = neg.getroottree().getpath(neg)
                                                # paths = path.split('/')
                                                # print(paths)
                                                print(get_depth(neg)[::-1])
                                                print(negation_events)

                        else:
                            pass

            # collect other words in the sentence
            elif element.get('wd'):
                pass
                # print(element.get('wd'))

    except TypeError:
        pass


for sentence in tree.findall('.//sentence'):
    elems = sentence.xpath('//negexp')
    negation_events = sum(1 for x in sentence.iter('neg_structure'))
    print(negation_events)

    for i in range(negation_events):
        process_sentence(sentence, i + 1, negation_events)

    print('***************************')
