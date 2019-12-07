""" This file contains utilities to convert arbitrary rules into CNF form, and to convert CNF trees back to original trees. """
from parsers import parse_Earley
from syntax1 import Sentence
from utility import Rule, Rules, Lexicon

def isCNF(rule):
    if not isinstance(rule, Rule):
        raise Exception("rule must be an instance of Rule class")
    return (len(rule.body) == 1 and isinstance(rule.body[0], str) or
            len(rule.body) == 2 and isinstance(rule.body[0], Lexicon) and isinstance(rule.body[1], Lexicon))

def convert2CNF(rules):
    """ takes a Rules instance, returns a converted Rules instance that abide with the CNF characteristics
    By convention, all auxiliary lexicons will start with '_', which is to be removed in the final parse tree """
    cnfRules = Rules()
    for rule in rules.getRules():
        if isCNF(rule):
            cnfRules.addRuleCopy(rule)
        elif len(rule.body) == 1:
            # case A => B
            # bubble an empty rule at the end of body
            # becomes A => B _X; _X => _
            pass
        elif len(rule.body) == 2:
            if (isinstance(rule.body[0], str)):
                # case A => w B
                # becomes A => _W B; _W => w
                pass
            else:
                # case A => B w
                # becomes A => B _W; _W => w
                pass
        else:
            # case A => B C .*
            # becomes A => _T; _T => B C; 
            pass

def deconvertCNF(cnfTree):
    # transform the cnftree in-place
    # base case: cnfTree has no children
    # recursive case
    for idx, child in enumerate(cnfTree.children):
        deconvertCNF(child)
        if child.name[0] == '_':
            cnfTree.children.pop(idx)
            cnfTree.children[idx:idx] = child.children





