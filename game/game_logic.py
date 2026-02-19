ROWS = 6
COLS = 7
EMPTY = ''
PLAYER1 = 'R'
PLAYER2 = 'Y'
PLAYERS = [PLAYER1, PLAYER2]
AVAILABLE_TOKENS = [PLAYER1, PLAYER2, 'G', 'B', 'P', 'O']
TOKEN_COLORS = {
    PLAYER1: 'red',
    PLAYER2: 'yellow',
    'G': 'green',
    'B': 'blue',
    'P': 'purple',
    'O': 'orange',
}


def new_board(rows=ROWS, cols=COLS):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def check_winner(board):
    rows = len(board)
    cols = len(board[0]) if board else 0
    for r in range(rows):
        for c in range(cols):
            p = board[r][c]
            if not p:
                continue
            # столб
            if c + 3 < cols and all(board[r][c + i] == p for i in range(4)):
                return p
            # строка
            if r + 3 < rows and all(board[r + i][c] == p for i in range(4)):
                return p
            # диаг вниз вправа
            if r + 3 < rows and c + 3 < cols and all(board[r + i][c + i] == p for i in range(4)):
                return p
            # диаг верх  вправо
            if r - 3 >= 0 and c + 3 < cols and all(board[r - i][c + i] == p for i in range(4)):
                return p
    return None


def apply_move(board, col, turn, players=None):

    if players is None:
        players = PLAYERS

    rows = len(board)
    placed = False
    for r in range(rows - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = turn
            placed = True
            break

    if not placed:
        return False, board, None, turn

    win = check_winner(board)
    if win:
        return True, board, win, turn

    try:
        idx = players.index(turn)
    except ValueError:
        next_turn = players[0]
    else:
        next_turn = players[(idx + 1) % len(players)]

    return True, board, None, next_turn
