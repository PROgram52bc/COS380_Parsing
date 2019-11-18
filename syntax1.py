from utility import Lexicon
from generator import randomSequence

# --- POS lexicons
Noun = Lexicon("Noun")
Noun.addRules("ideas", "warriors", "knowledge", "reproduction", "protection", "exhibition", "excellence", "education", "quality", "love","anger","hate", "peace","loyalty","integrity", "pride","courage","deceit", "honesty","trust","compassion", "bravery","misery","childhood","patriotism","friendship")

ProperNoun = Lexicon("ProperNoun")
ProperNoun.addRules("America's National Park System", "San Diego Zoo", "American Red Cross", "the U.S. Fund for UNICEF", "Donald Trump")

RelativePronoun = Lexicon("RelativePronoun")
RelativePronoun.addRules("that", "which", "of those who", "for those who", "through those who")

SubordinateConjunction = Lexicon("SubordinateConjunction")
SubordinateConjunction.addRules("as", "in order that", "on which", "by which", "through which")

Adjective = Lexicon("Adjective")
Adjective.addRules("excellent", "life-threatening", "poor", "better", "challenging", "natural", "lasting")

Verb = Lexicon("Verb")
Verb.addRules("create", "bring", "inspire", "increase", "mobilize", "undertake", "develop", "support", "engage in")

Preposition = Lexicon("Preposition")
Preposition.addRules("about", "below", "off", "toward", "above", "beneath", "for", "on", "under", "across", "beside", "from", "onto", "underneath", "after", "between", "in", "out", "until", "against", "beyond", "in front of", "outside", "up", "along", "but", "inside", "over", "upon", "among", "by", "in spite of", "past", "up to", "around", "concerning", "instead of", "regarding", "with", "at", "despite", "into", "since", "within", "because of", "down", "like", "through", "without", "before", "during", "near", "throughout", "with regard to", "behind", "of", "to", "with respect to")

# --- Recursive lexicons
PrepositionalPhrase = Lexicon("PrepositionalPhrase")
PrepositionalPhrase.addRule(Preposition, Noun)

NounPhrase = Lexicon("NounPhrase")
NounPhrase.addRule("the", Noun)
NounPhrase.addRule(Adjective, Noun)
NounPhrase.addRule(ProperNoun)
NounPhrase.addRule("the", Noun, "and", Noun)

VerbPhrase = Lexicon("VerbPhrase")
VerbPhrase.addRule(Verb)
VerbPhrase.addRule(Verb, "and", Verb)

SubordinateClause = Lexicon("SubordinateClause")
SubordinateClause.addRule(RelativePronoun, VerbPhrase, NounPhrase)
SubordinateClause.addRule(SubordinateConjunction, NounPhrase, VerbPhrase, NounPhrase)

Statement = Lexicon("Statement")
Statement.addRule("to", VerbPhrase, NounPhrase, SubordinateClause)
Statement.addRule("to", VerbPhrase, PrepositionalPhrase, "to", VerbPhrase, NounPhrase)
Statement.addRule("we", VerbPhrase, NounPhrase, PrepositionalPhrase)

if __name__ == "__main__":
    print(randomSequence(Statement))
