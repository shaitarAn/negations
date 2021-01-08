# !/usr/bin/env python3
# -*- coding: utf8 -*-

import spacy
from spacy.tokens import Doc

nlp = spacy.load('en_core_web_sm')

test = [["I", "'m", "never", "without", "one", "or", "the", "other",
         "before", "me", "."], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]]

desired_output = [["I", "'m"], ["without", "one", "or", "the", "other", "before", "me"]]

scope_tokens = []

span = []

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

doc = nlp(' '.join(test[0]))

for ind, token in enumerate(test[1]):
    if token == 0:
        scope_tokens.append(span)
        begin = doc[span[0]].idx
        end = doc[span[-1]].idx + len(doc[span[-1]].text)-1
        print(begin, end)
        span = []
    else:
        span.append(ind)


print(scope_tokens)

for i in doc:
    print(i.text, i.idx)
