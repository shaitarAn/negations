# !/usr/bin/env python3
# -*- coding: utf8 -*-

import xml.etree.ElementTree as ET

infile = 'corpora/box_rus.xml'
outfile = "output/russianBox.txt"

tree = ET.parse(infile)
root = tree.getroot()

with open(outfile, 'w') as outf:
    for sentence in root.findall('s'):
        if sentence.text:
            outf.write(sentence.text.strip() + '\n')
