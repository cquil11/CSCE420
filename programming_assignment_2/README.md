# PA2: Minimax for Tic-Tac-Toe
---
Author: Cameron Quilici, 630004248
Date: March 21, 2023
---

In this repository, you can find all my code, transcripts, and results for programming assignment 2 (CSCE 420, T. Ioerger, Spring 2023).

## Command Line Interface

In this section, you will find instructions on how to run the program `tty.py`.

To run the main program (Tic-Tac-Toe), enter the following into the terminal:

```
python3 ttt.py
```

There are no command line arguments that are passed in. All user interaction with the program is done during gameplay.

### Show

Shows the current state of the board. Example usage:
```
> show
O X . 
X . . 
. . . 
```

### Reset

Resets the board state and then shows the subsequent state of the board (empty). Example usage:
```
> show
O X . 
X O . 
. . . 

> reset
. . . 
. . . 
. . . 
```

### Move

Executed in the format `move <piece> <row> <column>`. Moves the specified piece to the specified row (A, B, C) column (1, 2, 3) position on the board and then displays the subsequent changes. Example usage:
```
> show
O X . 
X . . 
. . . 

> move O B 2
O X . 
X O . 
. . . 
```

### Choose

Executed in the format `choose <piece>`. Runs `minimax` with the specified piece ("X" or "O") as the maximizing player. Displays the minimax scores for each of the possible initial moves for `<piece>` at the top level. Also prints out the total number of nodes searched (how many total times `minscore` and `maxscore` were called during execution). Finally, prints out results of subsequent move chosen by the computer. Example usage:
```
> choose X
move (A, 1) mm_score: 0
move (B, 1) mm_score: 0
move (C, 1) mm_score: 0
move (A, 2) mm_score: 0
move (B, 2) mm_score: 0
move (C, 2) mm_score: 0
move (A, 3) mm_score: 0
move (B, 3) mm_score: 0
move (C, 3) mm_score: 0
number of nodes searched: 549946
X . . 
. . . 
. . . 
```

### Pruning
Executed in the format `pruning [state]` where `[state]` is the optional argument either `"on"` or `"off"` which triggers the `is_pruning` variable to be turned either on or off, respectively. Both return the current state of the pruning variable. Example usage:
```
Welcome to Tic-Tac-Toe
. . . 
. . . 
. . . 

> pruning on
Pruning is on
> pruning off
Pruning is off
> pruning
Pruning is off
```

### Set

Executed in the format `set <config>` where `<config>` is the specified state of the board in ASCII format. That is, a single string of pieces ("X" and "O") or empty-space characters (".") with no spaces that represent the board in row-major order. Displays the subsequent changes to the board after execution. Example usage:
```
Welcome to Tic-Tac-Toe
. . . 
. . . 
. . . 

> set XO..X..OO
X O . 
. X . 
. O O 
```

### Quit
Quits the program. Example usage:
```
> set XO..X..OO
X O . 
. X . 
. O O 

> quit
```
