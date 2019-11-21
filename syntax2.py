from utility import Lexicon
from generator import randomSequence, randomTree, tree2Sequence
from pptree import print_tree

# --- POS lexicons

Pronoun = Lexicon("Pronoun")
Pronoun.addRules("You", "I", "we")
ProperNoun = Lexicon("ProperNoun")
ProperNoun.addRules("Dr. Nurkkala")

SubjectNoun = Lexicon("SubjectNoun")
SubjectNoun.addRule(Pronoun)
SubjectNoun.addRule(ProperNoun)

ObjectNoun = Lexicon("ObjectNoun")
ObjectNoun.addRules("flight", "book")

Noun = Lexicon("Noun")
Noun.addRule(SubjectNoun)
Noun.addRule(ObjectNoun)

Article = Lexicon("Article").addRules("the", "a")

Verb = Lexicon("Verb")
Verb.addRules("book", "carry")

VerbPhrase = Lexicon("VerbPhrase")
VerbPhrase.addRule(Verb, Article, ObjectNoun)
VerbPhrase.addRule(Verb, "and", Verb)
VerbPhrase.addRule(Verb)

Sentence = Lexicon("Sentence")
Sentence.addRule(SubjectNoun, VerbPhrase)

if __name__ == "__main__":
    tree = randomTree(Sentence)
    print_tree(tree)
    sequence = tree2Sequence(tree)
    print(" ".join(sequence))
