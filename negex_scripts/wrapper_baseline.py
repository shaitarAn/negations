# !/usr/bin/env python3
# -*- coding: utf8 -*-

# python3 wrapper_baseline.py OneScopeFR.json

from negex_baseline import sortRules, negTagger
import numpy as np
import sys
import json
from sklearn.metrics import classification_report

# json file with sentences and true scope labels
js = sys.argv[1]

outfile = format('sentCuesScopes_CAS_negex_one_scope.txt')


def main():
    true_scopes = []
    pred_scopes = []
    test_sents = []
    neg_scopes = []
    counter = 0
    with open(js) as json_file:
        counter = 0
        data = json.load(json_file)
        for sent in data:
            # print(sent)
            true_scopes.append(sent[2])
            # s = sent[0]
            s = ' '.join(sent[0])
            test_sents.append('\t'.join([str(counter), s]))
            counter += 1
    with open('CAS_cues.txt', 'rb') as rfile:
        irules = sortRules(rfile)
        for report in test_sents:
            report = report.split('\t')
            tagger = negTagger(sentence=report[1], rules=irules)
            numscopes = tagger.getNumericScopes()
            pred_scopes.append(numscopes)
            neg_scopes.append(tagger.getScopes())

    testdata = zip(test_sents, true_scopes, pred_scopes, neg_scopes)
    scopes = zip(test_sents, true_scopes, pred_scopes, neg_scopes)

    with open(outfile, 'w', encoding='utf8') as outf:
        for z in testdata:
            sent = z[0].split('\t')
            # outf.write(sent[1] + '\n')
            # outf.write(str(z[1]) + '\n')
            # outf.write(str(z[2]) + '\n')
            # outf.write(str(z[3]) + '\n')
            # outf.write('\n')

            # sent = z[0].split('\t')
            print(sent[1])
            print(z[1])
            print(z[2])
            print(z[3])
            print()

    t_scopes = []
    p_scopes = []

    for item in scopes:
        if len(item[1]) == len(item[2]):
            t_scopes.append(item[1])
            p_scopes.append(item[2])

    correct_flat = [item for sublist in t_scopes for item in sublist]
    predicted_flat = [item for sublist in p_scopes for item in sublist]

    y_true = np.array(correct_flat)
    y_pred = np.array(predicted_flat)
    print(classification_report(y_true, y_pred, digits=4))


if __name__ == '__main__':
    main()
