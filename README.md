# How to test the syntax file

All syntax files are named following the pattern of `syntax*.py`, for existing syntax files, running
```
python3 [syntaxfile.py]
```
will output a randomly generated tree and the corresponding sentence for that syntax

# How to parse a sentence

Parse algorithms are defined in `parsers.py`

parse function such as `parse_Earley` takes two parameters: 
1. `root` is a `Lexicon` object, usually a `Sentence` lexicon
1. `sequence`: is a list of strings, representing the sequence of the words in the sentence to be parsed

it returns a list of parse trees (as the root node of the tree). When parse failed, it returns an empty list

# Running the test cases

```
python3 test.py
```
