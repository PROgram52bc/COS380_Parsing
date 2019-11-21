from utility import Lexicon

Pronoun = Lexicon("Pronoun")
Pronoun.addRules("you", "I", "we")

DirectObject = Lexicon("DirectObject")
DirectObject.addRules("her", "duck")

PossessivePronoun = Lexicon("PossessivePronoun")
PossessivePronoun.addRules("her")

Adjective = Lexicon("Adjective")
Adjective.addRules("duck")

Verb = Lexicon("Verb")
Verb.addRules("saw")

Sentence = Lexicon("Sentence")
Sentence.addRule(Pronoun, Verb, DirectObject, Adjective)
Sentence.addRule(Pronoun, Verb, PossessivePronoun, DirectObject)
