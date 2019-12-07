from syntax_ambiguous import Sentence as SentenceAmbiguous
from syntax1 import Sentence as Sentence1
from syntax2 import Sentence as Sentence2
from syntaxL1 import Sentence as SentenceL1
from parsers import parse_Earley
from pptree import print_tree

lexicons = [
        SentenceAmbiguous, 
        Sentence1, 
        Sentence2, 
        SentenceL1
        ]

sequences = [
        "we saw her duck",
        "to bring before compassion to mobilize excellent reproduction",
        "we carry and book",
        "does NWA prefer meal on a Houston flight"
        ]
sequences = [ s.split(" ") for s in sequences ] # caveat: original sentences cannot have token with space in between (e.g. "Dr. Nurkkala")

def main():
    for i, (lexicon, sequence) in enumerate(zip(lexicons, sequences)):
        print()
        print("Test case {}:".format(i+1))
        print()
        print("*"*50)
        print()
        print("Sentence:", " ".join(sequence))
        print("Parse result(s):")
        trees = parse_Earley(lexicon, sequence)
        if trees:
            for idx, tree in enumerate(trees):
                print("Parse result {}:".format(idx+1))
                print_tree(tree)
        else:
            print("failed to parse")


main()
