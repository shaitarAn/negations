# !/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import sys

# python3 cue_diversity.py all_data_2Qlabels/FRENCH_2labels.json

# all_data_2Qlabels/spanishALL_2labels.json

infile = sys.argv[1]


def count_cues(infile):

    cues = []
    with open(infile) as df:
        data = json.load(df)

        for line in data:
            cue = ''
            sent = zip(line[0], line[1], line[2])
            for s in sent:
                if s[1] == 2:
                    cue += s[0] + ' '
                elif s[1] == 1:
                    cue = s[0]
            cues.append(cue.lower().strip())
    for item in set(cues):
        print(item)

    print(len(cues), len(set(cues)))

    print(len(data))


count_cues(infile)
