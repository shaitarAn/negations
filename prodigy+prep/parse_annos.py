import json
from spacy.lang.ru import Russian
from pathlib import Path
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS

nlp = Russian()
russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')


file = "rus_anno/russian_anno.db.jsonl"

scope_sents = []
scope_cues = []
data_scope = []


def write_files(data):

    outpath = Path('../russian/output/')
    outpath.mkdir(parents=True, exist_ok=True)

    outfile1 = outpath / Path('RUS.json')
    textfile1 = outpath / Path('RUS_sents.txt')
    textfile2 = outpath / Path('RUS_anno.txt')

    # for item in data:
    #     print(item)

    with open(outfile1, 'w') as outf1:
        json.dump(data, outf1)

    with open(textfile1, 'w', encoding='utf8') as outf:
        for item in data:
            outf.write(' '.join(item[0]) + '\n')

    count = 0
    with open(textfile2, 'w', encoding='utf8') as outf:
        for item in data:
            zipped = zip(item[0], item[1], item[2])
            cue = ''
            scope = ''
            for t in zipped:
                if t[1] != 3:
                    cue += ' ' + str(t[0])
                if t[2] != 0:
                    scope += ' ' + str(t[0])
            count += 1
            # outf.write(str(count) + '\t' + str(item[3]) + '\n')
            outf.write(' '.join(item[0]) + '\n')
            outf.write(str(item[1]) + '\n')
            outf.write(str(item[2]) + '\n')
            outf.write(cue.strip() + '\n')
            outf.write(scope.strip() + '\n')
            outf.write('\n')


with open(file, 'r') as json_file:
    json_list = list(json_file)

for json_str in json_list:
    result = json.loads(json_str)

    if 'spans' in result:
        rus_sent = nlp(result['text'])
        rus_sents = [t.text for t in rus_sent]
        # print(len(rus_sents), rus_sents)

        cues = [3] * len(rus_sent)
        scopes = [0] * len(rus_sent)

        cue_span = []
        scope_span = []

        for dict in result['spans']:
            # print(dict)

            if dict['label'] == 'Cue':
                # cues = []
                token_start = dict['token_start']
                token_end = dict['token_end']
                cue_span.append(rus_sent[token_start:token_end + 1])

                for i, t in enumerate(rus_sent):
                    if token_start <= i <= token_end:
                        # print(i, t)
                        cues[i] = 1

            if dict['label'] == 'Scope':
                token_start = dict['token_start']
                token_end = dict['token_end']
                scope_span.append(rus_sent[token_start:token_end + 1])
                for i, t in enumerate(rus_sent):
                    if token_start <= i <= token_end:
                        scopes[i] = 1

        # print([t.text for t in cue_span])
        # print([t.text for t in scope_span])
        # print(len(cues), cues)
        # print(len(scopes), scopes)
        # print()

        scope_sents.append(rus_sents)
        scope_cues.append(cues)
        data_scope.append(scopes)

# for item in scope_sents:
#     print([t.decode('utf-8') for t in item])

zipped_data = list(zip(scope_sents, scope_cues, data_scope))
write_files(zipped_data)
