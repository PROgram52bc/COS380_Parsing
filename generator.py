import random
import itertools

def randomSequence(lexicon):
    """ get a random list of words from a single lexicon or string """
    print(lexicon)
    if isinstance(lexicon, str):
        return [lexicon]
    rule = random.choice(lexicon.getRules())
    items = [ randomSequence(l) for l in rule.body ]
    return list(itertools.chain(*items))

