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


# counts the number of parents to the root element
def get_depth(element):
    # from https://stackoverflow.com/questions/39112938/parse-hierarchical-xml-tags
    depth = 0
    parent = element.getparent()
    path = [element.tag, parent.tag]
    while parent is not None:
        depth += 1
        parent = parent.getparent()
        if parent is not None:
            path.append(parent.tag)

    return path


pattern = re.compile('neg_structure\\[(.)')

for sentence in tree.findall('.//sentence'):
    elems = sentence.xpath('//negexp')
    negation_events = sum(1 for x in sentence.iter('neg_structure'))
    print(negation_events)
    for elem in elems:
        num = 0
        # print([x.tag for x in elem.iterancestors()][::-1])
        path = elem.getroottree().getpath(elem)
        paths = path.split('/')
        if pattern.search(path):
            num = pattern.search(path).group(1)
            # print(num)
        # negs = sum(1 for x in paths if x == 'neg_structure')
        negs = sum(1 for x in get_depth(elem) if x == 'neg_structure')
        # print('{}'.format(' > '.join(paths)))
        print('top level neg_structure #{}, depth of neg_structure:{}, neg_structures in sentence:{}'.format(
            num, negs, negation_events))
        print()
    print('***************************')
