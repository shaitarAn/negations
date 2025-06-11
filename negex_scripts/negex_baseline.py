import re


def sortRules(ruleList):
    """Return sorted list of rules.

    Rules should be in a tab-delimited format: 'rule\t\t[four letter negation tag]'
    Sorts list of rules descending based on length of the rule,
    splits each rule into components, converts pattern to regular expression,
    and appends it to the end of the rule. """
    ruleList = list(ruleList)
    ruleList.sort(key=len, reverse=True)
    sortedList = []
    for rule in ruleList:
        rule = rule.decode('iso8859-1')
        s = rule.strip().split('\t')
        splitTrig = s[0].split()
        trig = r'\s+'.join(splitTrig)
        pattern = r'\b(' + trig + r')\b'
        s.append(re.compile(pattern, re.IGNORECASE))
        sortedList.append(s)
    return sortedList


class negTagger(object):
    '''Take a sentence and tag negation terms and negated phrases.

    Keyword arguments:
    sentence -- string to be tagged
    phrases  -- list of phrases to check for negation
    rules    -- list of negation trigger terms from the sortRules function
    negP     -- tag 'possible' terms as well (default = True)    '''

    def __init__(self, sentence='', rules=None):
        self.__sentence = sentence
        self.__rules = rules
        self.__negTaggedSentence = ''
        self.__scopesToReturn = []
        self.numeric_scopes = []
        self.len = len(sentence.split())

        filler = '_'

        self.__sentence = re.sub(r" n' ", r' ne ', self.__sentence)
        self.__sentence = re.sub(r" d' ", r' de ', self.__sentence)
        for rule in self.__rules:
            reformatRule = re.sub(r'\s+', filler, rule[0].strip())
            self.__sentence = rule[3].sub(' ' + rule[2].strip()
                                          + reformatRule
                                          + rule[2].strip() + ' ', self.__sentence)

        overlapFlag = 0
        prenFlag = 0
        postFlag = 0

        ########################################################
        # check for [PREN]

        sentenceTokens = self.__sentence.split()
        self.numeric_scopes = [0] * (len(self.__sentence.split()))
        sentencePortion = ''
        aScopes = []
        tokens = []
        sb = []
        mwes = []
        for i in range(len(sentenceTokens)):

            if sentenceTokens[i][:6] == '[PREN]':
                prenFlag = 1
                overlapFlag = 0
                tokens.append(sentenceTokens[i])

            if sentenceTokens[i][:6] in ['[CONJ]', '[PSEU]', '[POST]']:
                overlapFlag = 1
                tokens.append(sentenceTokens[i])

            if i + 1 < len(sentenceTokens):
                if sentenceTokens[i + 1][:6] == '[PREN]':
                    overlapFlag = 1
                    tokens.append(sentenceTokens[i])
                    if sentencePortion.strip():
                        self.numeric_scopes[i] = 1
                        sentencePortion += ' ' + sentenceTokens[i]
                        aScopes.append(sentencePortion.strip())
                    sentencePortion = ''

            if prenFlag == 1 and overlapFlag == 0:
                sentencePortion = sentencePortion + ' ' + sentenceTokens[i]
                if sentenceTokens[i][:6] in ['[PREN]', '[PREP]', '[POST]'] and '_' in sentenceTokens[i]:
                    negtriglen = len(sentenceTokens[i].split('_'))
                    mwes.append((i, negtriglen))

                if sentenceTokens[i][:6] not in ['[PREN]', '[PREP]', '[POST]', '[CONJ]']:
                    if i == len(sentenceTokens) - 1 and sentenceTokens[i] == '.':
                        self.numeric_scopes[i] = 0
                    else:
                        self.numeric_scopes[i] = 1

            sb.append(sentenceTokens[i])

        if sentencePortion.strip():
            aScopes.append(sentencePortion.strip())

        for ind in mwes:
            index, length = ind
            for n in range(1, length):
                self.numeric_scopes.insert(index + n, 0)

        if len(self.numeric_scopes) < self.len:
            for i in range(len(sentenceTokens)):
                if sentenceTokens[i][:6] == '[CONJ]'and '_' in sentenceTokens[i]:
                    negt = len(sentenceTokens[i].split('_'))
                    for n in range(1, negt):
                        self.numeric_scopes.insert(i + n, 0)

        ########################################################
        # Check for [POST]

        sentencePortion = ''
        # reverse sentences in order to look for scope PRECEEDING the trigger
        sb.reverse()
        sentenceTokens = sb
        sb2 = []
        self.numeric_scopes.reverse()

        for i in range(len(sentenceTokens)):
            if sentenceTokens[i][:6] == '[POST]':
                postFlag = 1
                overlapFlag = 0

            if sentenceTokens[i][:6] in ['[CONJ]', '[PSEU]', '[PREN]']:
                overlapFlag = 1

            if i + 1 < len(sentenceTokens):
                if sentenceTokens[i + 1][:6] == '[POST]':
                    overlapFlag = 1
                    self.numeric_scopes[i] = 0
                    if sentencePortion.strip():
                        self.numeric_scopes[i] = 1
                        aScopes.append(sentencePortion.strip())
                    sentencePortion = ''

            if postFlag == 1 and overlapFlag == 0:
                sentencePortion = sentenceTokens[i] + ' ' + sentencePortion
                if sentenceTokens[i][:6] not in ['[PREN]', '[POST]']:
                    self.numeric_scopes[i] = 1

            sb2.insert(0, sentenceTokens[i])

        if sentencePortion.strip():
            aScopes.append(sentencePortion.strip())

        self.numeric_scopes.reverse()

        self.__negTaggedSentence = self.__negTaggedSentence.replace(filler, ' ')

        for line in aScopes:
            tokensToReturn = []
            thisLineTokens = line.split()
            for token in thisLineTokens:
                tokensToReturn.append(token)
            self.__scopesToReturn.append(' '.join(tokensToReturn))

    def getNegTaggedSentence(self):
        return self.__negTaggedSentence

    def getScopes(self):
        return self.__scopesToReturn

    def getNumericScopes(self):
        return self.numeric_scopes

    def __str__(self):
        text = self.__negTaggedSentence
        text += '\t' + '\t'.join(self.__scopesToReturn)
