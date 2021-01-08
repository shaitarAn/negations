# !/usr/bin/env python3
# -*- coding: utf8 -*-

import xml.etree.ElementTree as ET


article = format('../datasets/sp_SFU_Review_SP_NEG/peliculas/yes_4_12.tbf.xml')

allsentences = []
allscopes = []
allcues = []
count_all_sents = 0
count_neg_sents = 0
no_negs = 0

tree = ET.parse(article)
root = tree.getroot()

scopesnums = []


def find_cue(element):
    if element.tag == 'negexp' and element.attrib:
        for neg in list(element):
            resolve_multiword_cue(neg)
    elif element.tag == 'negexp':
        for neg in list(element):
            resolve_regular_cue(neg)

    elif element.get('wd'):
        sentences.append(
            element.get('wd'))
        scopes.append(1)
        cues.append(3)


def resolve_multiword_cue(neg):
    if neg.get('wd'):
        cue = neg.get('wd')
        for c in cue.split('_'):
            sentences.append(c)
            scopes.append(0)
            cues.append(2)

    elif neg.tag == 'event':
        for n in list(neg):
            if n.get('wd'):
                cue = n.get('wd')
                for c in cue.split('_'):
                    sentences.append(c)
                    scopes.append(0)
                    cues.append(2)


def resolve_regular_cue(neg):
    if neg.get('wd'):
        cue = neg.get('wd')
        if '_' in cue:
            for c in cue.split('_'):
                sentences.append(c)
                scopes.append(0)
                cues.append(2)
        else:
            sentences.append(neg.get('wd'))
            scopes.append(0)
            cues.append(1)

    elif neg.tag == 'event':
        for n in list(neg):
            if n.get('wd'):
                cue = n.get('wd')
                if '_' in cue:
                    for c in cue.split('_'):
                        sentences.append(c)
                        scopes.append(0)
                        cues.append(2)
                else:
                    # print('YAYAYAYA')
                    sentences.append(cue)
                    scopes.append(0)
                    cues.append(1)


def process_neg_structure(el_in_neg_structure):
    # process scope
    if el_in_neg_structure.tag == 'scope':
        for el_in_scope in list(el_in_neg_structure):

            # if cue is a multiword it has attribute 'discid="1n/c"'
            if el_in_scope.tag == 'negexp' and el_in_scope.attrib:
                for neg in list(el_in_scope):
                    resolve_multiword_cue(neg)

            # regular cue has no attribute
            elif el_in_scope.tag == 'negexp':
                for neg in list(el_in_scope):
                    resolve_regular_cue(neg)

            # event is part of the scope
            elif el_in_scope.tag == 'event':
                for event in list(el_in_scope):
                    find_cue(event)

            # find neg_structures nested in the scope chunk:
            elif el_in_scope.tag == 'neg_structure':
                for neg_structure_in_scope in list(el_in_scope):

                    # continue down the rabbit hole
                    if neg_structure_in_scope.tag == 'scope':
                        for s in list(neg_structure_in_scope):

                            # cue is not scope
                            if s.tag == 'negexp' and s.attrib:
                                for neg in list(s):
                                    resolve_multiword_cue(neg)
                            elif s.tag == 'negexp':
                                for neg in list(s):
                                    resolve_regular_cue(neg)
                            # futher down the hole
                            elif s.tag == 'event':
                                for ev in list(s):

                                    # we are down here now:
                                    # neg_structure -> scope -> neg_structure ->
                                    # scope -> event -> cue
                                    find_cue(ev)

                            # event words still in scope
                            elif s.get('wd'):
                                sentences.append(s.get('wd'))
                                scopes.append(1)
                                cues.append(3)

                    # words in neg_structure -> scope -> neg_structure
                    # should be scope
                    elif neg_structure_in_scope.get('wd'):
                        sentences.append(
                            neg_structure_in_scope.get('wd'))
                        scopes.append(1)
                        cues.append(3)

            # other words in neg_structure -> scope
            # scope words
            elif el_in_scope.get('wd'):
                sentences.append(el_in_scope.get('wd'))
                scopes.append(1)
                cues.append(3)

    # multiword cue in the neg_structure
    elif el_in_neg_structure.tag == 'negexp' and el_in_neg_structure.attrib:
        for neg in list(el_in_neg_structure):
            resolve_multiword_cue(neg)

    # regular cue in the neg_structure
    elif el_in_neg_structure.tag == 'negexp':
        for neg in list(el_in_neg_structure):
            resolve_regular_cue(neg)

    # event is not part of scope here
    # I saw only one case like this
    elif el_in_neg_structure.tag == 'event':
        for ev in list(el_in_neg_structure):
            sentences.append(ev.get('wd'))
            scopes.append(0)
            cues.append(3)

    # collect other words within the neg_structure
    elif el_in_neg_structure.get('wd'):
        sentences.append(el_in_neg_structure.get('wd'))
        scopes.append(0)
        cues.append(3)


for sentence in root.findall('sentence'):
    count_all_sents += 1
    negation_events = sum(1 for elem in sentence.iter() if elem.tag == 'neg_structure')

    if negation_events > 0:
        scopesnums.append(negation_events)
    try:
        sentences = []
        scopes = []
        cues = []
        for element in sentence:

            # top level neg_structures
            if element.tag == 'neg_structure':
                for el_in_neg_structure in list(element):

                    # process nested neg_structure
                    if el_in_neg_structure.tag == 'neg_structure':
                        for subsection in list(el_in_neg_structure):
                            process_neg_structure(subsection)

                    else:
                        # process elements of top level neg_structure
                        process_neg_structure(el_in_neg_structure)

            # collect other words in the sentence
            elif element.get('wd'):
                sentences.append(str(element.get('wd')))
                scopes.append(0)
                cues.append(3)

    except TypeError:
        pass

    if negation_events == 1:
        # count_neg_sents += 1
        # allcues.append(cues)
        # allscopes.append(scopes)
        # allsentences.append(sentences)
        print('ONESCOPE')
        # print(' '.join(sentences))
        # print(cues)
        # print(scopes)
        # print(len(sentences), len(cues), len(scopes))
        print()

    elif negation_events > 1:
        # count_neg_sents += 1
        print('MULTI')
        # print(' '.join(sentences))
        # print(cues)
        # print(scopes)
        # print(len(sentences), len(cues), len(scopes))
        print()
    else:
        print('NADA')
        print()
        no_negs += 1

# sentences = [" ".join([s for s in sent]) for sent in allsentences]
# print(sentences)

print(scopesnums)
