import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
from prodigy.util import split_string
from typing import List, Optional

from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS


# Recipe decorator with argument annotations: (description, argument type,
# shortcut, type / converter function called on value before it's passed to
# the function). Descriptions are also shown when typing --help.


@prodigy.recipe(
    "my.manual",
    dataset=("The dataset to use", "positional", None, str),
    spacy_model=("The base model", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    label=("One or more comma-separated labels", "option", "l", split_string),
    exclude=("Names of datasets to exclude", "option", "e", split_string),
)
def my_manual(
    dataset: str,
    spacy_model: str,
    source: str,
    label: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
):
    """
    Mark spans manually by token. Requires only a tokenizer and no entity
    recognizer, and doesn't do any active learning.
    """
    # Load the spaCy model for tokenization

    nlp = Russian()
    russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
    nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')

    # Load the stream from a JSONL file and return a generator that yields a
    # dictionary for each example in the data.
    stream = JSONL(source)
    # stream = json.loads(mytext)
    # stream = prodigy.get_stream(text, loader="txt")
    # stream = text

    # Tokenize the incoming examples and add a "tokens" property to each
    # example. Also handles pre-defined selected spans. Tokenization allows
    # faster highlighting, because the selection can "snap" to token boundaries.
    stream = add_tokens(nlp, stream)

    blocks = [
        # {"view_id": "html", "html_template": "<h5>{{versions}}</h5>"},
        {"view_id": "review"},  # plain text representation
        # {"view_id": "ner_manual"},  # better formatting and allows for highlighting
        # {"view_id": "html", "html_template": eval_html},
    ]

    return {
        "view_id": "blocks",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        # "exclude": exclude,  # List of dataset names to exclude
        "config": {  # Additional config settings, mostly for app UI
            # "lang": nlp.lang,
            "labels": label,  # Selectable label options
            "blocks": blocks,
        },
    }
