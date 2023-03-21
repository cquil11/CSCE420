import re
import copy

# Define legal commands as constants.
MOVE = "MOVE"
CHOOSE = "CHOOSE"
QUIT = "QUIT"
RESET = "RESET"
PRUNING = "PRUNING"
SET = "SET"
SHOW = "SHOW"

# Define global variables.
is_pruning = False
nodes_searched = 0
pieces = ["X", "O"]

# Dictionary that maps the valid moves to indices of a Board.
moves_list = {"A": 0, "B": 1, "C": 2, "1": 0, "2": 1, "3": 2}

# Regex patterns that represent all possible terminal winning states for "X".
terminal_patterns_x = [
    r"^X.{3}X.{3}X$",
    r"^XXX.{6}$",
    r"^.{3}XXX.{3}$",
    r"^.{6}XXX$",
    r"^.X..X..X.",
    r"^X.{2}X.{2}X.{2}",
    r"^..X..X..X",
    r"^..X.X.X..",
]

# Regex patterns that represent all possible terminal winning states for "O".
terminal_patterns_o = [
    r"^O.{3}O.{3}O$",
    r"^OOO.{6}$",
    r"^.{3}OOO.{3}$",
    r"^.{6}OOO$",
    r"^O.{2}O.{2}O.{2}",
    r"^.O..O..O.",
    r"^..O..O..O",
    r"^..O.O.O..",
]


class Board:
    """Represents a Board object which has a board."""

    def __init__(self, values=None) -> None:
        """By default, initialize board to an empty board. Otherwise, initialize to the ASCII
        representation of the board passed into values."""

        if values is None:
            self.board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        else:
            self.board = values

    def __str__(self) -> str:
        """Prints the board in a standard 3x3 Tic-Tac-Toe format."""

        board_ascii = ""
        for row in self.board:
            for piece in row:
                board_ascii = board_ascii + piece + " "
            board_ascii = board_ascii + "\n"
        return board_ascii

    def player_move(self, piece, row, column):
        """Sets the specified index of the board (via a dictionary) to the specified piece."""

        if piece not in pieces:
            print("Please pick a valid piece to play")
            return
        elif (
            row not in moves_list.keys()
            or column not in moves_list.keys()
            or self.board[moves_list[row]][moves_list[column]] != "."
        ):
            print("Illegal move specified")
            return

        self.board[moves_list[row]][moves_list[column]] = piece

    def is_terminal(self):
        """Checks if the board is in a terminal state by converting the board to a ASCII representation
        (single string with no spaces of all positions [A1A2A3B1B2B3C1C2C3]). Uses a dictionary of regular
        expressions to check if the current board state is winning for a player, or if it is a draw. Returns
        a tuple where the first value denotes if the board is in a terminal state and the second value denotes
        which player won or if it is a draw."""

        # Translate the state into a string for regex matching
        b_str = ""
        for row in self.board:
            for elem in row:
                b_str = b_str + elem

        # If the state is a terminal state, return true and which player the
        # terminal state favors (as a tuple), otherwise return false
        for pattern in terminal_patterns_x:
            if re.match(pattern, b_str):
                return True, "X"
        for pattern in terminal_patterns_o:
            if re.match(pattern, b_str):
                return True, "O"

        if "." not in b_str:
            return True, "draw"

        return False, None

    def reset(self):
        """Resets the state of the board."""
        self.board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

    def show(self):
        """Prints the board in a standard 3x3 Tic-Tac-Toe format."""
        print(self)


def minimax_search(state, player):
    """The initial function called to run minimax. State is the initial state passed in and player
    specifies the maximizing player. Returns the final minimax score and move accepted."""

    value, move = maxscore(state, player, player, 0, -10000000, 10000000)
    return move, value


def maxscore(state, cur_player, orig_player, depth, alpha, beta):
    """Takes in a state, current player, original player, depth, and alpha/beta values. Recursively calls
    minscore() until a terminal state has been reached. Maximizes the utility score for the orig_player.
    Returns the accepted utility score as well as the accepted move."""

    global nodes_searched, is_pruning
    nodes_searched += 1

    terminal_check = state.is_terminal()

    # Modified utility function
    if terminal_check[0]:
        if terminal_check[1] == orig_player:
            return 1 - 0.1 * depth, None
        elif terminal_check[1] == "draw":
            return 0, None
        return -1 + 0.1 * depth, None

    v = -100000000

    move = None

    for succ in generate_successors(state, cur_player):
        # Must generate successors of opposite player for next level.
        if cur_player == "X":
            v2, a2 = minscore(succ[0], "O", orig_player,
                              depth + 1, alpha, beta)
        else:
            v2, a2 = minscore(succ[0], "X", orig_player,
                              depth + 1, alpha, beta)

        if depth == 0:
            print(
                "move ("
                + str(chr(65 + succ[1][1]))
                + ", "
                + str(succ[1][0] + 1)
                + ") mm_score: "
                + str(v2)
            )

        if v2 > v:
            v = v2
            move = succ[0]
            alpha = max(alpha, v)
        if is_pruning:
            if v >= beta:
                return v, move

    return v, move


def minscore(state, cur_player, orig_player, depth, alpha, beta):
    """Takes in a state, current player, original player, depth, and alpha/beta values. Recursively calls
    maxscore() until a terminal state has been reached. Minimizes the utility score for the orig_player
    (that is, maximizes the utility score for the opponent).Returns the accepted utility score as well
    as the accepted move."""

    global nodes_searched, is_pruning
    nodes_searched += 1

    terminal_check = state.is_terminal()

    # Modified utility function
    if terminal_check[0]:
        if terminal_check[1] == orig_player:
            return 1 - 0.1 * depth, None
        elif terminal_check[1] == "draw":
            return 0, None
        return -1 + 0.1 * depth, None

    v = 100000000

    move = None
    for succ in generate_successors(state, cur_player):
        # Must generate successors of opposite player for next level.
        if cur_player == "X":
            v2, a2 = maxscore(succ[0], "O", orig_player,
                              depth + 1, alpha, beta)
        else:
            v2, a2 = maxscore(succ[0], "X", orig_player,
                              depth + 1, alpha, beta)
        if v2 < v:
            v = v2
            move = succ[0]
            beta = min(beta, v)
        if is_pruning:
            if v <= alpha:
                return v, move

    return v, move


def generate_successors(state, player):
    """Generates a list of successors of the current state of a Board. Each element
    of the list contains a tuple of a Board and a tuple of the move taken to generate said Board."""

    successors = []
    for row in range(len(state.board)):
        # Loops through each position in state and generates new Board for each empty position
        # (moves for specified player).
        for col in range(len(state.board[0])):
            if state.board[row][col] == ".":
                # Make a deep copy so current board isn't modified
                current_board = copy.deepcopy(state.board)
                if player == "X":
                    current_board[row][col] = "X"
                else:
                    current_board[row][col] = "O"
                successors.append((Board(current_board), (row, col)))
    return successors


def main():
    global nodes_searched, is_pruning

    # Initialize the current state of the game board.
    state = Board()

    print("Welcome to Tic-Tac-Toe")
    state.show()

    # Game continues until a player wins, the user specifies "quit", or a draw occurs.
    while True:
        user_move = input("> ").split(" ")

        # Main command line interface. Basic error checking is implemented. Most invalid
        # commands should be caught.
        if QUIT == user_move[0].upper():
            return
        elif (
            SET == user_move[0].upper()
            and len(user_move) == 2
            and len(user_move[1]) == 9
        ):
            i = 0
            for row in range(len(state.board)):
                for col in range(len(state.board[0])):
                    state.board[row][col] = user_move[1][i]
                    i += 1
            state.show()
        elif MOVE == user_move[0].upper() and len(user_move) == 4:
            state.player_move(user_move[1], user_move[2], user_move[3])
            state.show()
        elif CHOOSE == user_move[0].upper() and len(user_move) == 2:
            new_state = minimax_search(state, user_move[1])
            # Important. Changes the main game state to the new one chosen by the computer.
            state = copy.deepcopy(new_state[0])
            print("number of nodes searched: " + str(nodes_searched))
            nodes_searched = 0
            state.show()
        elif RESET == user_move[0].upper():
            state.reset()
            state.show()
        elif PRUNING == user_move[0].upper():
            if len(user_move) == 1:
                if is_pruning:
                    print("Pruning is on")
                else:
                    print("Pruning is off")
            elif (
                len(user_move) == 2
                and user_move[1].upper() == "ON"
                or user_move[1].upper() == "OFF"
            ):
                if user_move[1].upper() == "OFF":
                    is_pruning = False
                    print("Pruning is off")
                else:
                    is_pruning = True
                    print("Pruning is on")
        elif SHOW == user_move[0].upper() and len(user_move) == 1:
            state.show()
        else:
            print("Unrecognized command")

        # At the end of each iteration, check to see if the game has reached a terminal state.
        # If it has, quit the game.
        terminal_check = state.is_terminal()
        if terminal_check[0]:
            print(state)
            if terminal_check[1] == "draw":
                print("It's a draw")
            else:
                print("Player " + terminal_check[1] + " wins")
            return


if __name__ == "__main__":
    main()
