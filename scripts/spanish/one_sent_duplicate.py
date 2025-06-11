# !/usr/bin/env python3
# -*- coding: utf8 -*-

__author__ = "Anastassia Shaitarova"

# python3 duplicate_sents_ES.py

import xml.etree.ElementTree as ET
from pathlib import Path

outpath = Path('output/')
outpath.mkdir(parents=True, exist_ok=True)

article = format('test.xml')

tree = ET.parse(article)
root = tree.getroot()


def find_cues(element, negs, i):
    sentences = []
    scopes = []
    cues = []

    if element.tag == 'negexp' and element.attrib:
        for neg in list(element):
            tok, scope, cue = resolve_multiword_cue(neg)
            if negs == i:
                print('neg?_multi: {} in neg_structure #{}, turn {}'.format(
                    tok, negs, i))
                sentences.append(tok + '_' + str(negs))
            else:
                sentences.append(tok)
            scopes.append(scope)
            cues.append(cue)

    elif element.tag == 'negexp':
        for neg in list(element):
            tok, scope, cue = resolve_regular_cue(neg)
            if negs == i:
                print('neg?_simple: {} in neg_structure #{}, turn {}'.format(
                    tok, negs, i))
                sentences.append(tok + '_' + str(negs))
            else:
                sentences.append(tok)
            scopes.append(scope)
            cues.append(cue)

    elif element.tag == 'neg_structure':
        negs += 1

        if i == negs:
            a = 0
        else:
            a = 1

        for n in list(element):
            if n.tag == 'scope':
                for el in list(n):
                    if el.tag == 'negexp' and el.attrib:
                        for neg in list(el):
                            if neg.get('wd'):
                                cue = neg.get('wd')
                                for c in cue.split('_'):
                                    if negs == i:
                                        print('negD_multi: {} in neg_structure #{}, turn {}'.format(
                                            cue, negs, i))
                                        sentences.append(c + '_' + str(negs))
                                    else:
                                        sentences.append(c)
                                    scopes.append(0 + a)
                                    cues.append(2 + a)

                    # regular cue has no attribute
                    elif el.tag == 'negexp':
                        for neg in list(el):
                            if neg.get('wd'):
                                if negs == i:
                                    # print(neg.getparent())
                                    print('negD_simple: {} in neg_structure #{}, turn {}'.format(
                                        neg.get('wd'), negs, i))
                                    sentences.append(neg.get('wd') + '_' + str(negs))
                                else:
                                    sentences.append(neg.get('wd'))
                                scopes.append(1 + a)
                                cues.append(3 + a)

                    # event is part of the scope
                    elif el.tag == 'event':
                        for event in list(el):
                            # if negs == i:
                            #     sentences.append(event.get('wd') + '_' + str(negs))
                            # else:
                            sentences.append(event.get('wd'))
                            scopes.append(1 + a)
                            cues.append(3 + a)
                    else:
                        sentences.append(el.get('wd'))
                        scopes.append(1 + a)
                        cues.append(3 + a)
            else:
                sentences.append(n.get('wd'))
                scopes.append(1 + a)
                cues.append(3 + a)

    elif element.get('wd'):
        sentences.append(element.get('wd'))
        scopes.append(1)
        cues.append(3)

    return (sentences, scopes, cues, negs)


def resolve_multiword_cue(neg):
    if neg.get('wd'):
        cue = neg.get('wd')
        for c in cue.split('_'):
            return (c, 0, 2)

    elif neg.tag == 'event':
        for n in list(neg):
            if n.get('wd'):
                cue = n.get('wd')
                for c in cue.split('_'):
                    return (c, 0, 2)


def resolve_regular_cue(neg):
    if neg.get('wd'):
        cue = neg.get('wd')
        if '_' in cue:
            for c in cue.split('_'):
                return (c, 0, 2)
        else:
            return (neg.get('wd'), 0, 1)

    elif neg.tag == 'event':
        for n in list(neg):
            if n.get('wd'):
                cue = n.get('wd')
                if '_' in cue:
                    for c in cue.split('_'):
                        return (c, 0, 2)
                else:
                    return (cue, 0, 1)


def process_neg_structure(el_in_neg_structure, negs, i):

    sentences = []
    scopes = []
    cues = []

    # process scope
    if el_in_neg_structure.tag == 'scope':
        # print('*** beginning of scope ***')
        for el_in_scope in list(el_in_neg_structure):

            # if cue is a multiword it has attribute 'discid="1n/c"'
            if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                for neg in list(el_in_scope):
                    tok, scope, cue = resolve_multiword_cue(neg)
                    if negs == i:
                        print('neg1_inscope_multi: {} in neg_structure #{}, turn {}'.format(
                            tok, negs, i))
                        sentences.append(tok + '_' + str(negs))
                    else:
                        sentences.append(tok)
                    scopes.append(scope + negs)
                    cues.append(cue + negs)

            # regular cue has no attribute
            elif el_in_scope.tag == 'negexp':
                for neg in list(el_in_scope):
                    tok, scope, cue = resolve_regular_cue(neg)
                    if negs == i:
                        print('neg1_inscope_simple: {} in neg_structure #{}, turn {}'.format(
                            tok, negs, i))
                        sentences.append(tok + '_' + str(negs))
                    else:
                        sentences.append(tok)
                    scopes.append(scope + negs)
                    cues.append(cue + negs)

            # event is part of the scope
            elif el_in_scope.tag == 'event':
                for event in list(el_in_scope):
                    tok, scope, cue, n = find_cues(event, negs, i)
                    # sentences += tok
                    if n == i:
                        sentences += [t + '_' + str(n) for t in tok]
                        scopes += [s + n for s in scope]
                        cues += [c + n for c in cue]
                    else:
                        sentences += tok
                        scopes += [s + n for s in scope]
                        cues += [c + n for c in cue]

                    # negs = n

            # find neg_structures nested in the scope chunk:
            elif el_in_scope.tag == 'neg_structure':

                # print('negs2, i', negs, i)

                for neg_structure_in_scope in list(el_in_scope):
                    negs += 1

                    # continue down the rabbit hole
                    if neg_structure_in_scope.tag == 'scope':
                        for s in list(neg_structure_in_scope):

                            # cue is not scope
                            if s.tag == 'negexp' and s.attrib:
                                for neg in list(s):
                                    tok, scope, cue = resolve_multiword_cue(neg)
                                    if negs == i:
                                        print('neg2_multi: {} in neg_structure #{}, turn {}'.format(
                                            tok, negs, i))
                                        sentences.append(tok + '_' + str(negs))
                                    else:
                                        sentences.append(tok)
                                    scopes.append(scope + negs)
                                    cues.append(cue + negs)

                            elif s.tag == 'negexp':
                                for neg in list(s):
                                    tok, scope, cue = resolve_regular_cue(neg)
                                    if negs == i:
                                        print('neg2_simple: {} in neg_structure #{}, turn {}'.format(
                                            tok, negs, i))
                                        sentences.append(tok + '_' + str(negs))
                                    else:
                                        sentences.append(tok)
                                    scopes.append(scope + negs)
                                    cues.append(cue + negs)

                            # futher down the hole
                            elif s.tag == 'event':
                                for ev in list(s):

                                    # we are down here now:
                                    # neg_structure -> scope -> neg_structure ->
                                    # scope -> event -> cue
                                    tok, scope, cue, n = find_cues(ev, negs, i)
                                    if n == i:
                                        sentences += [t + '_' + str(n) for t in tok]
                                        scopes += [s + n for s in scope]
                                        cues += [c + n for c in cue]
                                    else:
                                        sentences += tok
                                        scopes += scope
                                        cues += cue
                                    # negs = n

                            # event words still in scope
                            elif s.get('wd'):
                                sentences.append(s.get('wd'))
                                scopes.append(1 + negs)
                                cues.append(3 + negs)

                    # words in neg_structure -> scope -> neg_structure
                    # should be scope
                    elif neg_structure_in_scope.get('wd'):
                        sentences.append(neg_structure_in_scope.get('wd'))
                        scopes.append(1 + negs)
                        cues.append(3 + negs)

            # other words in neg_structure -> scope
            # scope words
            elif el_in_scope.get('wd'):
                # print('SCOPE words', el_in_scope.get('wd'))
                sentences.append(el_in_scope.get('wd'))
                scopes.append(1 + negs)
                cues.append(3 + negs)

        # print('*** end of scope ***')

    # multiword cue in the neg_structure
    elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
        for neg in list(el_in_neg_structure):
            tok, scope, cue = resolve_multiword_cue(neg)
            if negs == i:
                print('neg1_multi: {} in neg_structure #{}, turn {}'.format(
                    tok, negs, i))
                sentences.append(tok + '_' + str(negs))
            else:
                sentences.append(tok)
            scopes.append(scope)
            cues.append(cue)

    # regular cue in the neg_structure
    elif el_in_neg_structure.tag == 'negexp':
        for neg in list(el_in_neg_structure):
            tok, scope, cue = resolve_regular_cue(neg)
            if negs == i:
                print('neg1_simple: {} in neg_structure #{}, turn {}'.format(
                    tok, negs, i))
                sentences.append(tok + '_' + str(negs))
            else:
                sentences.append(tok)
            scopes.append(scope)
            cues.append(cue)

    # event is not part of scope here
    # I saw only one case like this
    elif el_in_neg_structure.tag == 'event':
        for ev in list(el_in_neg_structure):
            # if negs == i:
            #     print('neg1_simple: {} in neg_structure #{}, turn {}'.format(
            #         tok, negs, i))
            #     sentences.append(ev.get('wd') + '_' + str(negs))
            # else:
            sentences.append(ev.get('wd'))
            scopes.append(0)
            cues.append(3)

    # collect other words within the neg_structure
    elif el_in_neg_structure.get('wd'):
        sentences.append(el_in_neg_structure.get('wd'))
        scopes.append(0)
        cues.append(3)

    return (sentences, scopes, cues, negs)


def process_sentence(sentence, i):

    tokens = []
    scopes = []
    cues = []
    negs = 0
    try:
        for element in sentence:

            # top level neg_structures
            if element.tag == 'neg_structure':
                negs += 1
                for el_in_neg_structure in list(element):

                    # process nested neg_structure
                    if el_in_neg_structure.tag == 'neg_structure':
                        negs += 1
                        for subsection in list(el_in_neg_structure):
                            sentences, scops, cus, negs = process_neg_structure(
                                subsection, negs, i)
                            tokens += sentences
                            scopes += scops
                            cues += cus

                    else:
                        # process elements of top level neg_structure
                        sentences, scops, cus, negs = process_neg_structure(
                            el_in_neg_structure, negs, i)
                        tokens += sentences
                        scopes += scops
                        cues += cus

            # collect other words in the sentence
            elif element.get('wd'):
                tokens.append(str(element.get('wd')))
                scopes.append(0)
                cues.append(3)

    except TypeError:
        pass

    return (tokens, scopes, cues)


def main():

    # #on the server
    # article = format('../corpora/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')

    # #localy
    # article = format('../datasets/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')

    one_scope_sents = []
    one_scope_scopes = []
    one_scope_cues = []
    one_scope_text_tokens = []

    multisents = []
    multiscopes = []
    multicues = []
    multi_text_tokens = []

    count_all_sents = 0
    count_neg_sents = 0
    count_neg_structures_all = 0

    for sentence in root.findall('sentence'):
        count_all_sents += 1

        reslist = list(sentence.iter())
        text = ' '.join([x.get('wd') for x in reslist if x.get('wd')])
        text_tokens = [x.get('wd') for x in reslist if x.get('wd')]

        # count negation structures in sentence
        negation_events = sum(1 for elem in sentence.iter()
                              if elem.tag == 'neg_structure')
        count_neg_structures_all += negation_events

        # print(type(sentence))
        print()
        for i in range(negation_events):
            tokens, scopes, cues = process_sentence(sentence, i+1)

            try:
                if negation_events == 1:
                    # print('T:', text)
                    print('t:', ' '.join(tokens))
                    print()
                    count_neg_sents += 1
                    one_scope_sents.append(tokens)
                    one_scope_scopes.append(scopes)
                    one_scope_cues.append(cues)
                    one_scope_text_tokens.append(text_tokens)

                # collect sentences with multiple negation structures
                elif negation_events > 1:
                    # print('T2:', text)
                    print('t2:', ' '.join(tokens))
                    print()
                    count_neg_sents += 1
                    multisents.append(tokens)
                    multiscopes.append(scopes)
                    multicues.append(cues)
                    multi_text_tokens.append(text_tokens)

            except TypeError:
                continue

            print('number of neg_structures in this sent is: ', negation_events)
            print('=============================================================')

    zipped_one_scope = list(zip(one_scope_sents, one_scope_cues,
                                one_scope_scopes, one_scope_text_tokens))
    zipped_multi = list(zip(multisents, multicues, multiscopes, multi_text_tokens))
    all = zipped_one_scope + zipped_multi

    # for item in all:
    #     print(' '.join(item[0]))
    #     print(item[1])
    #     print(item[2])
    #     print(len(item[0]), len(item[1]), len(item[2]), len(item[3]))
    #     print()

    print('count_all_sents: ', count_all_sents)
    print('count_neg_sents: ', count_neg_sents)
    print('count_neg_structures_all: ', count_neg_structures_all)


if __name__ == "__main__":
    main()
