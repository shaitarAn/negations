# Negations: extended work

## Duplicating sentences with multiple negations in the Spanish and French corpora.

### Spanish corpus SFU ReviewSP-NEG


__one_sent_SFU2MultiBERT.py__: is written as a test script for only one file from the corpus. It extracts annotations the way I did it in my thesis. It does not split sentences with multiple negations.

__one_sent_duplicate.py__: I try to extract anno and duplicate sentences using ElementTree. I iterate through each sentence as many times as there are negation structures in total. I also order negation structures by counting them incrementally. If the order of a negation structure == the order of iteration, I collect the anno for the cue.

PROBLEM: The ordering is messed up when there are multiple neg_structures on one level. For example: [1][2][3] - [1] -[1]
ElementTree does not allow to access a parent node!

__try_this.py__: Attempt to do the job with lxml instead of ElementTree. lxml has an attribute .getparent() and also elem.getroottree().getpath(elem) This allows to account for all negation_structures in a sentence.

PROBLEM: .getroot() uses actual file as a root. I cannot find a way to use sentence node as a root.

__process_top_level_negs_SP.py__: A copy of __try_this.py__ which processes the entire Spanish corpus. Currently, it counts the number of top level neg_structures and creates as many copies of a sentence as there neg_structures.

Current stats:
- 3076 all_neg_sents
- 4113 newly collected sents
- 4327 all_neg_structures
- 4327 nested_neg_sents
- 214 lost neg_structures
- (in my thesis I had collected 2197 OneScope sents)
