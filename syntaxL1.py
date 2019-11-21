from utility import Lexicon
from generator import randomSequence, randomTree, tree2Sequence
from pptree import Node, print_tree

Det = Lexicon("Det")
Noun = Lexicon("Noun")
Verb = Lexicon("Verb")
Pronoun = Lexicon("Pronoun")
ProperNoun = Lexicon("ProperNoun")
Aux = Lexicon("Aux")
Preposition = Lexicon("Preposition")

Det.addRules("that", "this", "a")
Noun.addRules("book", "flight", "meal", "money")
Verb.addRules("book", "include", "prefer")
Pronoun.addRules("I", "she", "me")
ProperNoun.addRules("Houston", "NWA")
Aux.addRules("does")
Preposition.addRules("from", "to", "on", "near", "through")

PP = Lexicon("PP")

Nominal = Lexicon("Nominal")
Nominal.addRule(Pronoun)
Nominal.addRule(ProperNoun)
Nominal.addRule(Det, Nominal)

NP = Lexicon("NP")
NP.addRule(Nominal)
NP.addRule(Nominal, Noun)
NP.addRule(Nominal, PP)
NP.addRule(Noun)

PP.addRule(Preposition, NP)

VP = Lexicon("VP")
VP.addRule(Verb)
VP.addRule(Verb, NP)
VP.addRule(Verb, NP, PP)
VP.addRule(Verb, PP)
VP.addRule(VP, PP)


Sentence = Lexicon("Sentence")
Sentence.addRule(NP, VP)
Sentence.addRule(Aux, NP, VP)
Sentence.addRule(VP)


if __name__ == "__main__":
    tree = randomTree(Sentence)
    print_tree(tree)
    sequence = tree2Sequence(tree)
    print(" ".join(sequence))
