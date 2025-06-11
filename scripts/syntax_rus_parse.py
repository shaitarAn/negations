# !/usr/bin/env python3
# -*- coding: utf8 -*-

# import spacy
import spacy_udpipe
from spacy import displacy


text = "Мне никогда не случалось видеть свое имя в газетах."
# spacy_udpipe.download('ru')
nlp = spacy_udpipe.load("ru")

doc = nlp(text)
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.dep_)

displacy.serve(doc, style="dep")


# print(doc.dep_)
