from pptree import Node, print_tree
from syntax2 import Sentence
from utility import Rule, Lexicon
import copy

DEBUG=0

def parse_Earley(root, sequence):
    """ returns a list of nodes """
    class State:
        def __init__(self, rule, startIdx=0, endIdx=0, dotPos=0):
            self.rule = rule
            self.startIdx = startIdx
            self.endIdx = endIdx
            self.children = [] # children is a list of states
            if dotPos > len(rule.body):
                raise Exception("Dot position out of bound")
            self.dotPos = dotPos
        def __copy__(self):
            c = State(self.rule, self.startIdx, self.endIdx, self.dotPos)
            c.children = copy.copy(self.children) # children should be a distinct list, item can point to same states though
            return c
        def toNode(self):
            node = Node(self.rule.head.name)
            itChildState = iter(self.children)
            for lexicon in self.rule.body:
                if isinstance(lexicon, Lexicon): # if the next element in the rule is a lexicon
                    state = next(itChildState)
                    node.children.append(state.toNode()) # pop out a state from the children, and get node from it
                elif isinstance(lexicon, str): # if the next element in the rule is a string
                    node.children.append(Node(lexicon)) # create a node with that string
                else:
                    raise Exception("Unknown element in rule: {}".format(repr(lexicon)))
            return node
        def nextElement(self):
            """ returns the element next to the dot, None if Dot at the end """
            return self.rule.body[self.dotPos] if self.dotPos < len(self.rule.body) else None
        def __repr__(self):
            return "<State {} => {} [{}:{}]>".format(
                    self.rule.head.name,
                    self.rule.body[:self.dotPos] + ("•",) + self.rule.body[self.dotPos:],
                    self.startIdx, self.endIdx)
        def __eq__(self, other):
            if isinstance(other, State):
                return (self.rule == other.rule and
                        self.startIdx == other.startIdx and
                        self.endIdx == other.endIdx and
                        self.dotPos == other.dotPos)

    chart = [ [] for i in range(len(sequence)+1) ]
    trees = []

    def predict(state, chart):
        lexicon = state.nextElement()
        if not isinstance(lexicon, Lexicon):
            raise Exception("The next element in {} is not a Lexicon object: {}".format(repr(state), repr(lexicon)))
        for rule in lexicon.getRules():
            newState = State(rule)
            newState.startIdx = state.endIdx
            newState.endIdx = state.endIdx
            if newState not in chart[newState.endIdx]:
                if DEBUG:
                    print("predicting new state: {}".format(repr(newState)))
                chart[newState.endIdx].append(newState)

    def scan(state, chart):
        """ Scan all the possible rules for the next lexicon in 'state'
        compare string value with the next token in sequence 
        add a completed state if match and not already added """
        lexicon = state.nextElement()
        if not isinstance(lexicon, Lexicon):
            raise Exception("The next element in {} is not a Lexicon object: {}".format(repr(state), repr(lexicon)))
        for rule in lexicon.getRules(lambda rule: rule.isPOS()):
            if len(sequence) > state.endIdx and rule.body[0] == sequence[state.endIdx]:
                newState = State(rule)
                newState.startIdx = state.endIdx
                newState.endIdx = state.endIdx + 1
                newState.dotPos = 1
                if newState not in chart[newState.endIdx]:
                    if DEBUG:
                        print("scanning new state: {}".format(repr(newState)))
                    chart[newState.endIdx].append(newState)

    def advance(state, chart):
        """ Assume the next lexicon in 'state' is a string
        compare string with the next token in sequence
        add new state if match """
        lexicon = state.nextElement()
        if not isinstance(lexicon, str): # compare the underlying string
            raise Exception("The next element in {} is not a string object: {}".format(repr(state), repr(lexicon)))
        if len(sequence) > state.endIdx and lexicon == sequence[state.endIdx]:
            newState = copy.copy(state)
            newState.endIdx += 1
            newState.dotPos += 1
            if DEBUG:
                print("advancing new state: {}".format(repr(newState)))
            chart[newState.endIdx].append(newState)

    def complete(state, chart):
        for oldState in chart[state.startIdx]:
            if oldState.nextElement() == state.rule.head:
                newState = copy.copy(oldState)
                newState.endIdx = state.endIdx
                newState.dotPos += 1
                newState.children.append(state)
                if DEBUG:
                    print("completing new state: {}".format(repr(newState)))
                chart[newState.endIdx].append(newState)

    # Is there a way to eliminate the root state?
    rootRule = Rule(Lexicon(""), (root,))
    chart[0].append(State(rootRule))


    # compute states
    for i in range(len(chart)):
        for state in chart[i]:
            nextElement = state.nextElement()
            if nextElement is None:
                complete(state, chart)
            elif isinstance(nextElement, Lexicon):
                if nextElement.isPOS():
                    scan(state, chart)
                else:
                    predict(state, chart)
            elif isinstance(nextElement, str):
                advance(state, chart)
            else:
                raise Exception("Unknown next element: {}".format(repr(nextElement)))

    # collect completed trees
    for state in chart[-1]:
        if state.startIdx == 0 and \
            state.nextElement() is None and \
            state.rule is not rootRule:
            if DEBUG:
                print("Successfully parsed state", state, "with children:", state.children)
            trees.append(state.toNode())

    # example parse tree
    # Sentence = Node("Sentence")
    # Node("I", Node("Noun", Sentence))
    # VerbPhrase = Node("VerbPhrase", Sentence)
    # Node("eat", Node("Verb", VerbPhrase))
    # Node("dinner", Node("Noun", VerbPhrase))
    # trees.append(Sentence)

    return trees


if __name__ == "__main__":
    trees = parse_Earley(Sentence, ['Tom', 'fight', 'and', 'book'])
    for tree in trees:
        print_tree(tree)
