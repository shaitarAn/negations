# !/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import sys
from random import sample
# import re

__author__ = "Anastassia Shaitarova"

# python3 count_lexical_overlap.py vocabularies/english_bert_vocab.json vocabularies/multil_bert_vocab.txt vocabularies/bert-base-multilingual-cased_FR_vocab.json vocabularies/bert-base-multilingual-cased_SP_vocab.json vocabularies/bert-base-multilingual-cased_RUS_vocab.json

# python3 count_lexical_overlap.py vocabularies/xlm-roberta-base_ENG_vocab.json vocabularies/sentencepiece_vocab.txt vocabularies/xlm-roberta-base_FR_vocab.json vocabularies/xlm-roberta-base_SP_vocab.json vocabularies/xlm-roberta-base_RUS_vocab.json


infile = sys.argv[1]
infile2 = sys.argv[2]
infile3 = sys.argv[3]
infile4 = sys.argv[4]
infile5 = sys.argv[5]


with open(infile) as en, open(infile2, 'r') as vocab, open(infile3) as fr, open(infile4) as sp, open(infile5) as ru:
    dataen = json.load(en)
    datafr = json.load(fr)
    datasp = json.load(sp)
    dataru = json.load(ru)
    bert = [item.strip() for item in vocab]

    french_sample = [item.strip() for item in datafr]

    all = dataen + datafr + datasp + dataru

    # #print a random sample of mBERT's vocabulary
    print('    '.join(sample(french_sample, 800)))
    print('--------------')
    print('mBERT vocab size:', len(bert))
    print('vocab size english:', len(set(dataen)))
    print('vocab size french:', len(set(datafr)))
    print('vocab size spanish:', len(set(datasp)))
    print('vocab size russian:', len(set(dataru)))
    print()

    def find_lexical_overlap(train, test, a, b):
        intersection = set(train) & set(test)
        union = set(train + test)
        overlap = int(round((len(intersection) / len(union)), 2) * 100)
        print('--------------')
        print('Jaccard Index between {} and {} is {}:'.format(a, b, overlap))

        # print(len(intersection))
        # print(len(union))
        # print(len(union) / len(test) * 100)
        #
        print('{}% of {} is {}'.format(int(round(len(intersection) * 100 / len(train), 0)), a, b))
        print('{}% of {} is {}'.format(int(round(len(intersection) * 100 / len(test), 0)), b, a))
        print()

    find_lexical_overlap(dataen, datafr, 'en', 'fr')
    find_lexical_overlap(dataen, datasp, 'en', 'sp')
    find_lexical_overlap(dataen, datasp, 'en', 'ru')

    find_lexical_overlap(datafr, datasp, 'fr', 'sp')
    find_lexical_overlap(dataen, datasp, 'ru', 'sp')
    find_lexical_overlap(dataen, datafr, 'ru', 'fr')

    # #explore subwords constituting the cue 'négatif'
    # for item in bert:
    #     if 'gati' in item:
    #         print(item)

    # count
    # count = 0
    #
    # for item in sorted(set(all)):
    #     z = re.match('##\\w$', item)
    #     if z:
    #         count += 1
    #         # print(item)
    #
    # print(count)
    print(len(set(all)))
