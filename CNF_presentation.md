# CNF converter/deconverter

## Terminology & framework

-   lexicon: a non-terminal
-   terminals represented using string
-   head: the subject of a rule, a `lexicon`
-   body: the content of the rule, a `list` of `lexicon` or `string`s

## CNF format

-   `A` => `B` `C`

Non-terminal to 2 non-terminal

-   `W` => `w`

Non-terminal to 1 terminal

## Parse algorithm

-   parse algorithm takes a set of rules and the target sentence, and returns tree(s) representing the syntax of the sentence
-   Two tasks:
    1.  convert the rules into CNF
    1.  deconvert the trees to the original format

## Converter

> steps needed to convert an arbitrary rule set into CNF

### Goal: convert `A` => `arbitrary body` into `A` => `CNF body`

### 3 categories of `arbitrary body` and method for converting

#### 1. Eliminate method: `A` => `B`

for all `B` => `arbitrary body`

convert `A` => `arbitrary body`

#### 2. Wrap method: `A` => `B` `w` | `A` => `w` `B` | `A` => `w1` `w2`

wrap all terminals in body with a wrapper rule: `_W` => `w`

replace the terminals with the wrapper rule's head: `A` => `B` `_W`

> So far, we can handle all rules of length <= 2

#### 3. Split method: `A` => `X` `Y` `Z`\*

> where `X`, `Y`, `Z` are either terminal or non-terminal, in otherwords, body length > 2

add `A` => `_T1` `_T2`

convert `_T1` => `X` `Y` (This can be handled by Wrap method)

convert `_T2` => `Z`\*

## Reversibility

> Elimination method non-reversible

-   For case: `A` => `B`; `B` => `w`
-   Eliminate to `A` => `w` (There is no obvious way to encode the intermediate `B` lexicon in this rule)
-   But it is possible to have a `A` => `w` rule prior to conversion

## Bubble method?

-   Why not change that to: `A` => `B` `EMPTY`; `B` => `w`; `EMPTY` => `empty`
-   Bubble method not applicable since in CKY parser, we are always asking: "Can these two cells be combined together to become a rule?" and there will never be a cell with content '\_' that matches the bubbled rule

## Reverser

-   eliminate all nodes starting with an underscore, replace the node with its children

## Implementation/experimentation

> Used Earley parser, but should make no difference

-   Show correctly converted lexicons
-   Show loss of information due to elimination
