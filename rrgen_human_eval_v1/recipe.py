import random
import re

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens

import spacy
from spacy.tokenizer import Tokenizer

# NOTE: we just use the en model here since its purpose is
# to simply tokenize on white-space. Therefore, a
# language-specific model is not necessary.
nlp = spacy.load('./en_core_web_sm-2.3.1/en_core_web_sm/en_core_web_sm-2.3.1')
nlp.tokenizer = Tokenizer(nlp.vocab)


with open('eval_criteria.html', 'r', encoding='utf8') as f:
    eval_html = f.read()

with open('script.js', 'r', encoding='utf8') as f:
    javascript = f.read()

@prodigy.recipe('rrgen-human-eval')
def multi_eval_rrgen(dataset, file_path):

    stream = JSONL(file_path)
    stream = add_tokens(nlp, stream, skip=True)

    blocks = [
        {"view_id": "html", "html_template": "<h5>{{src}}</h5>"},
        # {"view_id": "text"}, # plain text representation
        {"view_id": "ner_manual"}, # better formatting and allows for highlighting
        {"view_id": "html", "html_template": eval_html},
    ]

    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": 'blocks',
        "config": {
            # "labels": ["RELEVANT"],
            "blocks": blocks, # add the blocks to the config
            "javascript": javascript,
        }
    }
