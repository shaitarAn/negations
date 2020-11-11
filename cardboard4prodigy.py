# !/usr/bin/env python3
# -*- coding: utf8 -*-


__author__ = "Anastassia Shaitarova"


import json
import re
import spacy
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup as BS
from spacy.tokens import Doc


anno = "test_sherlock.json"
# "output/SHERLOCK_cardbord.json"
parallels = "corpora/box.en.ru.txt"

rusent = re.compile(r'>(.*)<')
nlp = spacy.load('en_core_web_sm')


# https://spacy.io/usage/linguistic-features#native-tokenizers
class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)


nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)


with open(parallels, 'r') as p, open(anno, 'r') as a:
    data = json.load(a)
    for line in p:
        for sent in data:
            spans = []
            scopes = {}

            if ' '.join(sent[0]) in line and 0 not in sent[1]:
                line = line.strip().split('\t')
                mysent = ET.fromstring(line[0]).text
                doc = nlp(mysent)
                scope_tokens = []

                print(mysent)
                print(len(mysent.split()))

                for cue in sent[1]:
                    if cue != 3:
                        cues = {}
                        print(sent[1].index(cue))
                        print('LOOK HERE', doc[sent[1].index(cue)])
                        onset = doc[sent[1].index(cue)].idx
                        offset = onset + len(doc[sent[1].index(cue)].text)-1
                        cues["start"] = onset
                        cues["end"] = offset
                        cues["label"] = "CUE"
                        spans.append(cues)

                for ind, token in enumerate(sent[2]):
                    if token != 0:
                        scope_tokens.append(ind)

                begin = doc[scope_tokens[0]].idx
                end = doc[scope_tokens[-1]].idx + len(doc[scope_tokens[-1]].text)-1
                scopes["start"] = begin
                scopes["end"] = end
                scopes["label"] = "SCOPE"
                spans.append(scopes)
                print(scope_tokens)

                soup = BS(line[1], features="html.parser")
                russian = ''
                for s in soup.find_all('s'):
                    russian += s.text + ' '
                print(russian)

                print({
                    "text": russian,
                    "view_id": "ner_manual",
                    "versions": [{"text": mysent,
                                  "spans": spans}]
                })

                print()
