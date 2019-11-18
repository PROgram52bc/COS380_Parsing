import random
import itertools
from pptree import Node

def randomSequence(lexicon):
    """ get a random list of words from a single lexicon or string """
    if isinstance(lexicon, str):
        return [lexicon]
    rule = random.choice(lexicon.getRules())
    items = [ randomSequence(l) for l in rule.body ]
    return list(itertools.chain(*items))

def randomTree(lexicon):
    if isinstance(lexicon, str):
        return Node(lexicon)
    rule = random.choice(lexicon.getRules())
    n = Node(lexicon.name)
    n.children = [ randomTree(l) for l in rule.body ]
    return n
