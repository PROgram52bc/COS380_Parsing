""" This file contains utilities to convert arbitrary rules into CNF form, and to convert CNF trees back to original trees. """
from parsers import parse_Earley
from syntax1 import Sentence
from utility import Rule, Rules, Lexicon

def isCNF(rule):
    if not isinstance(rule, Rule):
        raise Exception("rule must be an instance of Rule class")
    return (len(rule.body) == 1 and isinstance(rule.body[0], str) or
            len(rule.body) == 2 and isinstance(rule.body[0], Lexicon) and isinstance(rule.body[1], Lexicon))

def convertCNF(rules):
    """ takes a Rules instance, returns a converted Rules instance that abide with the CNF characteristics
    By convention, all auxiliary lexicons will start with '_', which is to be removed in the final parse tree 
    auxiliary lexicons to be discarded entirely (without bringing up the children) will start with '__' """
    def getCounter():
        i = 0
        while True:
            yield i
            i += 1
    def _convert(rule, rules, counter):
        if isCNF(rule):
            rules.addRuleCopy(rule.head, rule.body)
        elif len(rule.body) == 1:
            # ELIMINATE method
            # case A => B, B => .*
            # becomes _convert(A => b) for all b in B
            for subrule in rule.body[0].getRules():
                _convert(Rule(rule.head, subrule.body), rules, counter)

            # # BUBBLE method requires modified parser
            # # case A => B
            # # bubble an empty rule at the end of body
            # # becomes A => B __X; __X => _
            # rules.addRuleCopy("__EMPTY", ("_",)) # add __EMPTY => _ into the collection
            # rules.addRuleCopy(rule.head, (rule.body[0], rules.getLexicon("__EMPTY"))) # add A => B __EMPTY into the collection
        elif len(rule.body) == 2:
            tmpHead1 = rules.getLexicon("_TMP{}".format(next(counter))) # create a new lexicon
            if (isinstance(rule.body[1], Lexicon)):
                # case A => w B
                # becomes A => _W B; _W => w
                rules.addRuleCopy(tmpHead1, (rule.body[0],)) # add _W => w into the collection
                rules.addRuleCopy(rule.head, (tmpHead1, rule.body[1])) # add A => _W B into the collection
            elif (isinstance(rule.body[0], Lexicon)):
                # case A => B w
                # becomes A => B _W; _W => w
                rules.addRuleCopy(tmpHead1, (rule.body[1],)) # add _W => w into the collection
                rules.addRuleCopy(rule.head, (rule.body[0], tmpHead1)) # add A => B _W into the collection
            else:
                # case A => w1 w2
                # becomes A => _W1 _W2; _W1 => w1; _W2 => w2
                tmpHead2 = rules.getLexicon("_TMP{}".format(next(counter))) # create a new lexicon
                rules.addRuleCopy(rule.head, (tmpHead1, tmpHead2)) # add A => _W1 _W2 into the collection
                rules.addRuleCopy(tmpHead1, (rule.body[0],)) # add _W1 => w1 into the collection
                rules.addRuleCopy(tmpHead2, (rule.body[1],)) # add _W2 => w2 into the collection
        else:
            # case A => X Y .*
            # becomes A => _T1 _T2; _convert(_T1 => X Y); _convert(_T2 => .*); 
            tmpHead1 = rules.getLexicon("_TMP{}".format(next(counter))) # create a new lexicon
            tmpHead2 = rules.getLexicon("_TMP{}".format(next(counter))) # create a new lexicon
            rules.addRuleCopy(rule.head, (tmpHead1, tmpHead2)) # add A => _T1 _T2 into the collection
            _convert(Rule(tmpHead1, rule.body[0:2]), rules, counter) # convert _T1 => X Y into the CNF and add to collection
            _convert(Rule(tmpHead2, rule.body[2:]), rules, counter) # convert _T2 => .* into CNF and add to collection

    cnfRules = Rules()
    counter = getCounter()
    for rule in rules.getRules():
        _convert(rule, cnfRules, counter)
    return cnfRules

def deconvertCNF(cnfTree):
    # transform the cnftree in-place
    # base case: cnfTree has no children
    # recursive case
    for idx, child in enumerate(cnfTree.children):
        deconvertCNF(child)
        if child.name[0:1] == '_': # using slice to silence index out of bound error
            cnfTree.children.pop(idx)
            if child.name[1:2] != '_':
                cnfTree.children[idx:idx] = child.children
