from copy import deepcopy


class Action:  # lawsuit
    row: int = 0
    col: int = 0
    sym: int = 0
    evaluation: int = 0

    def __init__(self, row: int, col: int, sym: int):
        self.row = row
        self.col = col
        self.sym = sym

    def __str__(self):
        act: str = f"Placing {'X' if self.sym == -1 else 'O'} at ({self.row}, {self.col})"
        return f"{act}: {self.evaluation}"

    def guistring(self) -> str:
        if self.col == 0:
            colstr: str = "A"
        elif self.col == 1:
            colstr: str = "B"
        else:
            colstr: str = "C"

        if self.evaluation == -1:
            ev: str = "X wins"
        elif self.evaluation == 0:
            ev: str = "Tie"
        elif self.evaluation == 1:
            ev: str = "O wins"
        else:
            ev: str = "undefined evaluation"

        return f"{'X' if self.sym == -1 else 'O'} at {colstr}{self.row+1}: {ev}"


class TicTacToe:
    board: list[list[int]] = [[0 for i in range(3)] for j in range(3)]

    def __init__(self, predef: list[list[int]]):
        self.board = predef

    def place(self, turn: bool, row: int, col: int) -> None:
        if turn:
            self.board[row][col] = -1  # Place an X
        else:
            self.board[row][col] = 1   # Place an O

    def ask_user_to_place(self, turn: bool) -> None:
        coords: list[int] = [int(s) for s in input(f"Enter x, y to place {'X' if turn else 'O'}: ").split(", ")]
        self.place(turn, coords[0], coords[1])

    def next_turn(self) -> None:
        on_board = [t for rows in self.board for t in rows]
        if on_board.count(1) == on_board.count(-1):
            self.ask_user_to_place(True)
        else:
            self.ask_user_to_place(False)


class InvalidBoardException(Exception):
    def __init__(self):
        super().__init__("Invalid board configuration.\nX's must be the same as, or 1 more than O's.")


def winner_of(board: TicTacToe) -> int:
    state = board.board
    rows: list[list[int]] = state
    cols: list[list[int]] = [[r[i] for r in state] for i in range(3)]
    diag: list[list[int]] = [[r[i] for i, r in enumerate(state)], [r[2-i] for i, r in enumerate(state)]]
    candidates: list[list[int]] = rows + cols + diag
    for cand in candidates:
        if set(cand) == {-1}:
            return -1  # X wins
        if set(cand) == {1}:
            return 1   # O wins
    if 0 not in [e for c in candidates for e in c]:
        return 0       # Draw
    else:
        return 2       # Incomplete


def next_to_place(board: TicTacToe) -> int:
    on_board = [t for rows in board.board for t in rows]
    return -1 if on_board.count(1) == on_board.count(-1) else 1


def actions(board: TicTacToe) -> list[Action]:
    player = next_to_place(board)
    possible_actions: list[Action] = []
    for ri, r in enumerate(board.board):
        for ci, c in enumerate(r):
            if c == 0:
                possible_actions.append(Action(ri, ci, player))
    return possible_actions


def result(board: TicTacToe, action: Action) -> TicTacToe:
    res = deepcopy(board)
    if action.sym == -1:
        res.place(True, action.row, action.col)
    else:
        res.place(False, action.row, action.col)
    return res


def minimax(board: TicTacToe, depth: int):
    evaluation: int = winner_of(board)

    if evaluation in [-1, 0, 1]:
        return evaluation

    if next_to_place(board) == -1:
        val = float("inf")
        for action in actions(board):
            val = min(val, minimax(result(board, action), depth + 1))
        return val

    if next_to_place(board) == 1:
        val = float("-inf")
        for action in actions(board):
            val = max(val, minimax(result(board, action), depth + 1))
        return val


def move_evaluations(board: TicTacToe):
    if not is_valid_board(board):
        raise InvalidBoardException
    possible_moves = actions(board)
    for action in possible_moves:
        action.evaluation = minimax(result(board, action), 0)
    return possible_moves


def is_valid_board(board: TicTacToe):
    on_board = [t for rows in board.board for t in rows]
    return on_board.count(1) in [on_board.count(-1), on_board.count(-1) - 1]


if __name__ == "__main__":
    test = TicTacToe([[1, 0, 1],
                      [0, -1, -1],
                      [-1, 1, 0]])
    for m in move_evaluations(test):
        print(str(m))