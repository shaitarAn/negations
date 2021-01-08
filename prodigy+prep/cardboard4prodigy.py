# !/usr/bin/env python3
# -*- coding: utf8 -*-


__author__ = "Anastassia Shaitarova"


import json
import re
import spacy
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup as BS
from spacy.tokens import Doc
import jsonlines

# russian sentences to annotate
anno = "output/SHERLOCK_cardbord.json"

# parallel Rus-Eng sentences
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


with open(parallels, 'r') as p, open(anno, 'r') as a, jsonlines.open('output.jsonl', mode='w') as writer:
    data = json.load(a)
    for line in p:
        for sent in data:
            spans = []

            if ' '.join(sent[0]) in line:
                 # and 0 not in sent[1]
                line = line.strip().split('\t')
                mysent = ET.fromstring(line[0]).text
                doc = nlp(mysent)

                cues = {}
                cue_chunk = []

                for ind, cue in enumerate(sent[1]):
                    if cue == 3 and len(cue_chunk) != 0:
                        onset = doc[cue_chunk[0]].idx
                        offset = doc[cue_chunk[-1]].idx + len(doc[cue_chunk[-1]].text)
                        cues["start"] = onset
                        cues["end"] = offset
                        cues["label"] = "CUE"
                        spans.append(cues)
                        cues = {}
                        cue_chunk = []
                    elif cue != 3:
                        cue_chunk.append(ind)

                scopes = {}
                scope_chunk = []

                for ind, token in enumerate(sent[2]):
                    if token == 0 and len(scope_chunk) != 0:
                        begin = doc[scope_chunk[0]].idx
                        end = doc[scope_chunk[-1]].idx + len(doc[scope_chunk[-1]].text)
                        scopes["start"] = begin
                        scopes["end"] = end
                        scopes["label"] = "SCOPE"
                        spans.append(scopes)
                        scope_chunk = []
                        scopes = {}
                    elif token != 0:
                        scope_chunk.append(ind)

                soup = BS(line[1], features="html.parser")
                russian = ''
                for s in soup.find_all('s'):
                    russian += s.text + ' '

                # "spans": [{"start": 93, "end": 120, "label": "SCOPE"}, {"start": 121, "end": 123, "label": "CUE"},{"start": 124, "end": 132, "label": "SCOPE"}]}]}
                spans = sorted(spans, key=lambda start: start['start'])

                print(({
                    "text": russian,
                    "view_id": "ner_manual",
                    "versions": [{"text": mysent,
                                  "spans": spans}]
                }))

                # writer.write({
                #     "text": russian,
                #     "view_id": "ner_manual",
                #     "versions": [{"text": mysent,
                #                   "spans": spans}]
                # })

        # line = line.split('\t')
        print(type(line))
        if isinstance(line, str):
            print('@@@', line)
        else:

            soup = BS(line[1], features="html.parser")
            russian = ''
            for s in soup.find_all('s'):
                russian += s.text + ' '
            print('+++', russian)
