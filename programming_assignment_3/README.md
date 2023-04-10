# PA3: DPLL

## Important Notes

The parsing of the `*.cnf` files can be a bit finnicky. There is not support for commenting lines of code "inline". Please avoid writing any functional instruction on the same line you have a comment in any `*.cnf` files. Further, there seem to be mistakes that occur when there is a space character at the end of lines in `*.cnf` files. If you notice something buggy with the parsing of clauses/propositions, make sure there are no erroneous spaces at the end of lines in any `*.cnf` files.

## Execution Instructions
Simply run
```
python3 dpll.py <filename> [literals]* [+UCH]
```
to run the program. The program assumes that the file specified exists, and of course that the specified additional literals are not nonsensical (i.e., they relate to the clauses in the specified KB).

## `generate-queens-cnf.py`

I made this script to generate my KBs for the n-queens problem. If you need to run it, simply execute
```
python3 generate-queens-cnf.py
```
and you will be prompted to enter a value for `n` which is the dimension of the queen problem you would like to generate a KB for. The program will automatically format these in a `<n>-queens.cnf` file where `n` is, again, the number specified by the user.