from pptree import Node, print_tree
from syntax2 import Statement
from utility import Rule, Lexicon

def parse_Earley(lexicon, sequence):
    """ returns a list of nodes """
    chart = [ [] for i in range(len(sequence)+1) ]
    trees = []
    class State:
        def __init__(self, rule, startIdx=0, endIdx=0, dotPos=0):
            self.rule = rule
            self.startIdx = startIdx
            self.endIdx = endIdx
            if dotPos > len(rule.body):
                raise Exception("Dot position out of bound")
            self.dotPos = dotPos
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

    def predict(state, states):
        lexicon = state.nextElement()
        if not isinstance(lexicon, Lexicon):
            raise Exception("Trying to apply predictor on a terminal {}".format(repr(lexicon)))
        for rule in lexicon.getRules():
            newState = State(rule, startIdx=state.endIdx, endIdx=state.endIdx)
            if newState not in states:
                print("Predict from ", state)
                print(newState)
                states.append(newState)

    def scan(state, states):
        lexicon = state.nextElement()
        if isinstance(lexicon, str): # compare the string to the next word in the sequence
            if lexicon == sequence[state.startIdx]:
                newState = State(state.rule, startIdx=state.startIdx, endIdx=state.endIdx+1, dotPos=state.dotPos+1)
                if newState not in states:
                    print("Scan with", lexicon)
                    print(newState)
                    states.append(newState)

#     def scanPOS(state, states):
#         if isinstance(lexicon, Lexicon): # compare the underlying string
#             rules = lexicon.getRules(lambda rule: rule.body[0] == sequence[state.startIdx])
#             if rules:
#                 rule = rules[0]
#                 newState = State(rule, startIdx=state.endIdx, endIdx=state.endIdx+1)
#                 print(newState)
#                 states.append(newState)

    def complete(completed, chart):
        for states in chart[:completed.endIdx+1]:
            for state in states:
                if state.nextElement() == completed.rule.head:
                    newState = State(state.rule, startIdx=state.startIdx, endIdx=completed.endIdx, dotPos=state.dotPos+1)
                    print("Complete with", completed)
                    print(newState)
                    chart[completed.endIdx].append(newState)

    # Is there a way to eliminate the root state?
    rootRule = Rule(Lexicon(""), (Statement,))
    chart[0].append(State(rootRule))

    for i in range(len(chart)):
        for state in chart[i]:
            nextElement = state.nextElement()
            if nextElement is None:
                complete(state, chart)
            elif isinstance(nextElement, Lexicon):
                predict(state, chart[i])
            elif isinstance(nextElement, str):
                if i < len(sequence):
                    scan(state, chart[i+1])
            else:
                raise Exception("Unknown next element: {}".format(repr(nextElement)))

    for state in chart[len(sequence)]:
        if state.startIdx == 0 and state.dotPos == len(state.rule.body):
            print(state)

    # Question: How does dynamic programming help with efficiency? What's the purpose of collecting the states in sets?
    # Where do the repeated states come from?

    # example parse tree
    Sentence = Node("Sentence")
    Node("I", Node("Noun", Sentence))
    VerbPhrase = Node("VerbPhrase", Sentence)
    Node("eat", Node("Verb", VerbPhrase))
    Node("dinner", Node("Noun", VerbPhrase))
    trees.append(Sentence)

    return trees


if __name__ == "__main__":
    trees = parse_Earley(Statement, ['I', 'book', 'flight'])
    for tree in trees:
        print_tree(tree)
