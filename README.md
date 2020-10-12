# Negations: extended work

## Duplicating sentences with multiple negations in the Spanish and French corpora.

### Spanish corpus SFU ReviewSP-NEG


__one_sent_SFU2MultiBERT.py__: is written as a test script for only one file from the corpus. It extracts annotations the way I did it in my thesis. It does not split sentences with multiple negations.

__one_sent_duplicate.py__: I try to extract anno and duplicate sentences using ElementTree. I iterate through each sentence as many times as there are negation structures in total. I also order negation structures by counting them incrementally. If the order of a negation structure == the order of iteration, I collect the anno for the cue.

PROBLEM: The ordering is messed up when there are multiple neg_structures on one level. For example: [1][2][3] - [1] -[1]
ElementTree does not allow to access a parent node!

__try_this.py__: Attempt to do the job with lxml instead of ElementTree. lxml has an attribute .getparent() and also elem.getroottree().getpath(elem) This allows to account for all negation_structures in a sentence.

PROBLEM: .getroot() uses actual file as a root. I cannot find a way to use sentence node as a root. 
