import re
import copy

# Define legal commands as constants
MOVE = "MOVE"
CHOOSE = "CHOOSE"
QUIT = "QUIT"
RESET = "RESET"
PRUNING = "PRUNING"
SET = "SET"

is_pruning = False
nodes_searched = 0

moves_list = {
    "A": 0,
    "B": 1,
    "C": 2,
    "1": 0,
    "2": 1,
    "3": 2
}

pieces = ["X", "O"]

terminal_patterns_x = [
    r"^X.{3}X.{3}X$",
    r"^XXX.{6}$",
    r"^.{3}XXX.{3}$",
    r"^.{6}XXX$",
    r"^.X..X..X.",
    r"^X.{2}X.{2}X.{2}",
    r"^..X..X..X",
    r"^..X.X.X.."
]

terminal_patterns_o = [
    r"^O.{3}O.{3}O$",
    r"^OOO.{6}$",
    r"^.{3}OOO.{3}$",
    r"^.{6}OOO$",
    r"^O.{2}O.{2}O.{2}",
    r"^.O..O..O.",
    r"^..O..O..O",
    r"^..O.O.O.."
]


class Board:

    def __init__(self, values=None) -> None:
        if values is None:
            self.board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        else:
            self.board = values

    def __str__(self) -> str:
        board_ascii = ""
        for row in self.board:
            for piece in row:
                board_ascii = board_ascii + piece + " "
            board_ascii = board_ascii + "\n"
        return board_ascii

    def player_move(self, piece, row, column):
        if piece not in pieces:
            print("Please pick a valid piece to play")
            return
        elif row not in moves_list.keys() or column not in moves_list.keys() \
                or self.board[moves_list[row]][moves_list[column]] != ".":
            print("Illegal move specified")
            return

        self.board[moves_list[row]][moves_list[column]] = piece

    def is_terminal(self):
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
        self.board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]


def minimax_search(state, player):
    value, move = maxscore(state, player, player, 0, -10000000, 10000000)
    return move, value


def maxscore(state, cur_player, orig_player, depth, alpha, beta):
    global nodes_searched, is_pruning
    nodes_searched += 1

    terminal_check = state.is_terminal()

    if terminal_check[0]:
        if terminal_check[1] == orig_player:
            return 1 - .1 * depth, None
        elif terminal_check[1] == "draw":
            return 0, None
        return -1 + .1 * depth, None

    v = -100000000

    move = None

    for succ in generate_successors(state, cur_player):
        if cur_player == "X":
            v2, a2 = minscore(succ[0], "O", orig_player,
                              depth + 1, alpha, beta)
        else:
            v2, a2 = minscore(succ[0], "X", orig_player,
                              depth + 1, alpha, beta)

        if depth == 0:
            print("move (" + str(chr(65 + succ[1][1])) + ", " +
                  str(succ[1][0] + 1) + ") mm_score: " + str(v2))

        if v2 > v:
            v = v2
            move = succ[0]
            alpha = max(alpha, v)
        if is_pruning:
            if v >= beta:
                return v, move

    return v, move


def minscore(state, cur_player, orig_player, depth, alpha, beta):
    global nodes_searched, is_pruning
    nodes_searched += 1

    terminal_check = state.is_terminal()

    if terminal_check[0]:
        if terminal_check[1] == orig_player:
            return 1 - .1 * depth, None
        elif terminal_check[1] == "draw":
            return 0, None
        return -1 + .1 * depth, None

    v = 100000000

    move = None
    for succ in generate_successors(state, cur_player):
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
    successors = []
    for row in range(len(state.board)):
        for col in range(len(state.board[0])):
            if state.board[row][col] == ".":
                current_board = copy.deepcopy(state.board)
                if player == "X":
                    current_board[row][col] = "X"
                else:
                    current_board[row][col] = "O"
                successors.append((Board(current_board), (row, col)))
    return successors


def main():
    global nodes_searched, is_pruning

    state = Board()

    print("Welcome to Tic-Tac-Toe")
    while True:
        print(state)
        user_move = input("> ").split(" ")

        # Main command line interface
        if QUIT == user_move[0].upper():
            return
        elif SET == user_move[0].upper() and len(user_move) == 2 and len(user_move[1]) == 9:
            i = 0
            for row in range(len(state.board)):
                for col in range(len(state.board[0])):
                    state.board[row][col] = user_move[1][i]
                    i += 1
        elif MOVE == user_move[0].upper() and len(user_move) == 4:
            state.player_move(user_move[1], user_move[2], user_move[3])
        elif CHOOSE == user_move[0].upper() and len(user_move) == 2:
            new_state = minimax_search(state, user_move[1])
            state = copy.deepcopy(new_state[0])
            print("number of nodes searched: " + str(nodes_searched))
            nodes_searched = 0
        elif RESET == user_move[0].upper():
            state.reset()
        elif PRUNING == user_move[0].upper():
            if len(user_move) == 1:
                if is_pruning:
                    print("Pruning is on")
                else:
                    print("Pruning is off")
            elif len(user_move) == 2 and user_move[1].upper() == "ON" \
                    or user_move[1].upper() == "OFF":
                if user_move[1].upper() == "OFF":
                    is_pruning = False
                    print("Pruning is off")
                else:
                    is_pruning = True
                    print("Pruning is on")
        else:
            print("Unrecognized command")

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
