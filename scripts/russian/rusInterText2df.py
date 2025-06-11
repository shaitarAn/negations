# !/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import re
import spacy
import pandas as pd
from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS

# input = sys.argv[1]
# output = sys.argv[2]

text = "Не ветер, а какой-то ураган!"
nlp = Russian()
doc = nlp(text)
russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')
doc = nlp(text)
print([token.text for token in doc])
# ['Не', 'ветер', ',', 'а', 'какой-то', 'ураган', '!']
# Notice that word "какой-то" remains a single token.


def test_sent():
    testSent = "Должен же быть какой-то смысл, иначе получается, что нашим миром управляет случай, а это немыслимо."
    nlp = spacy.load('ru2')
    nlp.add_pipe(nlp.create_pipe('sentencizer'), first=True)
    doc = nlp(testSent)
    russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
    nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')
    doc = nlp(testSent)
    for s in doc.sents:
        print(s)
        print([(t.lemma_, t.text, t.pos_, t.dep_) for t in s])


def process_text_spacyru2():
    '''
    Uses:
    - Russian tagging spacy model https://github.com/buriy/spacy-ru
    - https://github.com/aatimofeev/spacy_russian_tokenizer

    takes InterText aligned file and writes annotated Russian sentences to pandas dataframe

    '''
    sent = re.compile('>([-\u0410-\u044F\u0401\\w\\s.?!,";:]+)</s')
    id = re.compile('id="\\d:(\\d+)')
    text = []
    with open(input, 'r') as inf:
        for line in inf:
            line = line.split('\t')
            # print(line)
            s = sent.findall(line[1])
            s = ' '.join(s)
            i = id.search(line[0])
            if i:
                inum = int(i.group(1)) - 1
            else:
                inum = None
            nlp = spacy.load('ru2')
            nlp.add_pipe(nlp.create_pipe('sentencizer'), first=True)
            doc = nlp(s)
            russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
            nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')
            doc = nlp(s)
            sentence = []
            for se in doc.sents:
                count_tokens = 0
                for t in se:
                    sentence = [inum, count_tokens, t.text, t.lemma_, t.pos_]
                    text.append(sentence)
                    count_tokens += 1
                    print(sentence)
                sentence = []
                # text.append(sentence)

    df = pd.DataFrame(text[1:], columns=['sentence', 'token', 'word', 'lemma', 'pos'])
    df.to_csv(output)
    print(df)


# test_sent()
# process_text_spacyru2()
