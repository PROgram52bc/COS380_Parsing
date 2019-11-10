from components import Terminal, NonTerminal
# Custom classes

# --- Leaf components
class Noun(Terminal):
    pass
Noun.addToCollection("ideas", "warriors", "knowledge", "reproduction", "protection", "exhibition", "excellence", "education", "quality", "love","anger","hate", "peace","loyalty","integrity", "pride","courage","deceit", "honesty","trust","compassion", "bravery","misery","childhood","patriotism","friendship")

class ProperNoun(Terminal):
    pass
ProperNoun.addToCollection("America's National Park System", "San Diego Zoo", "American Red Cross", "the U.S. Fund for UNICEF", "Donald Trump")

class RelativePronoun(Terminal):
    pass
RelativePronoun.addToCollection("that", "which", "of those who", "for those who", "through those who")

class SubordinateConjunction(Terminal):
    pass
SubordinateConjunction.addToCollection("as", "in order that", "on which", "by which", "through which")

class Adjective(Terminal):
    pass
Adjective.addToCollection("excellent", "life-threatening", "poor", "better", "challenging", "natural", "lasting")

class Verb(Terminal):
    pass
Verb.addToCollection("create", "bring", "inspire", "increase", "mobilize", "undertake", "develop", "support", "engage in")

class Preposition(Terminal):
    pass
Preposition.addToCollection("about", "below", "off", "toward", "above", "beneath", "for", "on", "under", "across", "beside", "from", "onto", "underneath", "after", "between", "in", "out", "until", "against", "beyond", "in front of", "outside", "up", "along", "but", "inside", "over", "upon", "among", "by", "in spite of", "past", "up to", "around", "concerning", "instead of", "regarding", "with", "at", "despite", "into", "since", "within", "because of", "down", "like", "through", "without", "before", "during", "near", "throughout", "with regard to", "behind", "of", "to", "with respect to")

# --- Node components
class PrepositionalPhrase(NonTerminal):
    pass
PrepositionalPhrase.addConstruct(Preposition, Noun)

class NounPhrase(NonTerminal):
    pass
NounPhrase.addConstruct(Terminal("the"), Noun)
NounPhrase.addConstruct(Adjective, Noun)
NounPhrase.addConstruct(ProperNoun)
NounPhrase.addConstruct(Terminal("the"), Noun, Terminal("and"), Noun)

class VerbPhrase(NonTerminal):
    pass
VerbPhrase.addConstruct(Verb)
VerbPhrase.addConstruct(Verb, Terminal("and"), Verb)

class SubordinateClause(NonTerminal):
    pass
SubordinateClause.addConstruct(RelativePronoun, VerbPhrase, NounPhrase)
SubordinateClause.addConstruct(SubordinateConjunction, NounPhrase, VerbPhrase, NounPhrase)

class Statement(NonTerminal):
    pass
Statement.addConstruct(Terminal("to"), VerbPhrase, NounPhrase, SubordinateClause)
Statement.addConstruct(Terminal("to"), VerbPhrase, PrepositionalPhrase, Terminal("to"), VerbPhrase, NounPhrase)
Statement.addConstruct(Terminal("we"), VerbPhrase, NounPhrase, PrepositionalPhrase)


if __name__ == "__main__":
    st = Statement.random()
    print(str(st))
