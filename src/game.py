BOARD_SIZE = 8
EMPTY = "."

RED = "r"
RED_KING = "R"
BLACK = "b"
BLACK_KING = "B"


# Create the starting checkerboard
def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Black pieces start at the top
    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = BLACK

    # Red pieces start at the bottom
    for row in range(5, 8):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = RED

    return board


# Print the board with row and column numbers
def print_board(board):
    print()
    print("   0 1 2 3 4 5 6 7")
    print("  -----------------")

    for row in range(BOARD_SIZE):
        print(row, "|", end=" ")
        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")
        print()

    print()


# Check if coordinates are inside the board
def is_on_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


# Check if a piece belongs to the current player
def belongs_to_player(piece, player):
    if player == "red":
        return piece in (RED, RED_KING)

    if player == "black":
        return piece in (BLACK, BLACK_KING)

    return False


# Check whether a basic diagonal move is legal
def is_valid_move(board, start_row, start_col, end_row, end_col, player):
    if not is_on_board(start_row, start_col):
        return False

    if not is_on_board(end_row, end_col):
        return False

    piece = board[start_row][start_col]

    if piece == EMPTY:
        return False

    if not belongs_to_player(piece, player):
        return False

    if board[end_row][end_col] != EMPTY:
        return False

    row_change = end_row - start_row
    col_change = end_col - start_col

    if abs(col_change) != 1:
        return False

    if piece == RED:
        return row_change == -1

    if piece == BLACK:
        return row_change == 1

    if piece in (RED_KING, BLACK_KING):
        return abs(row_change) == 1

    return False


# Find the basic legal moves for one piece
def get_legal_moves(board, row, col, player):
    moves = []

    if not is_on_board(row, col):
        return moves

    piece = board[row][col]

    if not belongs_to_player(piece, player):
        return moves

    possible_moves = [
        (row - 1, col - 1),
        (row - 1, col + 1),
        (row + 1, col - 1),
        (row + 1, col + 1)
    ]

    for end_row, end_col in possible_moves:
        if is_valid_move(board, row, col, end_row, end_col, player):
            moves.append((end_row, end_col))

    return moves


# Move a piece to the new square
def make_move(board, start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]

    board[end_row][end_col] = piece
    board[start_row][start_col] = EMPTY


# Switch to the other player
def switch_player(player):
    if player == "red":
        return "black"

    return "red"


# Read move coordinates from the user
def read_move():
    print("Enter move as: start_row start_col end_row end_col")
    move = input("> ").strip().split()

    if len(move) != 4:
        return None

    try:
        values = [int(value) for value in move]
    except ValueError:
        return None

    return values


# Main command line game loop
def main():
    board = create_board()
    current_player = "red"

    print("Checkers")
    print("Rows and columns are numbered 0 through 7.")

    while True:
        print_board(board)

        print(current_player.capitalize() + "'s turn")

        move = read_move()

        if move is None:
            print("Invalid input. Enter four numbers from 0 to 7.")
            continue

        start_row, start_col, end_row, end_col = move

        if not is_valid_move(
            board,
            start_row,
            start_col,
            end_row,
            end_col,
            current_player
        ):
            print("Invalid move. Try again.")
            continue

        make_move(board, start_row, start_col, end_row, end_col)

        current_player = switch_player(current_player)


if __name__ == "__main__":
    main()