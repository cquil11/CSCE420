# PA3: DPLL

## Important Notes

Please see my comments in results/results.txt (where you will also find all of the collective data). Additionally, I did not see anywhere in the directions where it specified to upload the results of running dpll.py on an unsatisfiable instance of Map Coloring, so I didn't add that one.

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