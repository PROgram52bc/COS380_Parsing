from utility import Rule, Lexicon, Rules
from syntax1 import Sentence as Sentence1
from syntaxL1 import Sentence as SentenceL1
from generator import randomTree, randomSequence, tree2Sequence
from cnf_converter import deconvertCNF, convertCNF
from pptree import print_tree, Node
from parsers import parse_Earley


lexicons = [
        Sentence1,
        # SentenceL1,
        ]

sequences = [
        ("to", "increase", "and", "undertake", "the", "friendship", "of", "those", "who", "support", "American Red Cross"),
        # ("does", "NWA", "prefer", "meal", "on", "a", "Houston", "flight")
        ]

def main():
    for i, (lexicon, sequence) in enumerate(zip(lexicons, sequences)):
        print()
        print("Test case {}:".format(i+1))
        print()
        print("*"*50)
        print()
        print("Sentence:", " ".join(sequence))

        print("Original Parse result(s):")
        trees = parse_Earley(lexicon, sequence)
        for idx, tree in enumerate(trees):
            print("Parse result {}:".format(idx+1))
            print_tree(tree)
        print()

        print("CNF parse result(s):")
        rules = Rules().fromLexicon(lexicon)
        cnfRules = convertCNF(rules)
        cnfLexicon = cnfRules.getLexicon(lexicon.name)
        trees = parse_Earley(cnfLexicon, sequence)
        for idx, tree in enumerate(trees):
            print("CNF result {}:".format(idx+1))
            print_tree(tree)
        print()

        print("Deconverted CNF result(s):")
        for tree in trees:
            print("Deconverted result {}:".format(idx+1))
            deconvertCNF(tree)
            print_tree(tree)
        print()

main()
