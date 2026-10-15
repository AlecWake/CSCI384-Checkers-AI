BOARD_SIZE = 8
EMPTY = "."

RED = "r"
RED_KING = "R"
BLACK = "b"
BLACK_KING = "B"


# Create the starting checkerboard
def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = BLACK

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


def is_on_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def belongs_to_player(piece, player):
    if player == "red":
        return piece in (RED, RED_KING)

    if player == "black":
        return piece in (BLACK, BLACK_KING)

    return False


def belongs_to_opponent(piece, player):
    if player == "red":
        return piece in (BLACK, BLACK_KING)

    if player == "black":
        return piece in (RED, RED_KING)

    return False


# Get the directions a piece can move
def get_directions(piece):
    if piece == RED:
        return [(-1, -1), (-1, 1)]

    if piece == BLACK:
        return [(1, -1), (1, 1)]

    if piece in (RED_KING, BLACK_KING):
        return [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

    return []


# Find normal one-square moves
def get_simple_moves(board, row, col, player):
    moves = []

    if not is_on_board(row, col):
        return moves

    piece = board[row][col]

    if not belongs_to_player(piece, player):
        return moves

    for row_change, col_change in get_directions(piece):
        new_row = row + row_change
        new_col = col + col_change

        if is_on_board(new_row, new_col):
            if board[new_row][new_col] == EMPTY:
                moves.append((new_row, new_col))

    return moves


# Find captures available for one piece
def get_capture_moves(board, row, col, player):
    captures = []

    if not is_on_board(row, col):
        return captures

    piece = board[row][col]

    if not belongs_to_player(piece, player):
        return captures

    for row_change, col_change in get_directions(piece):
        middle_row = row + row_change
        middle_col = col + col_change

        end_row = row + (row_change * 2)
        end_col = col + (col_change * 2)

        if not is_on_board(end_row, end_col):
            continue

        if not is_on_board(middle_row, middle_col):
            continue

        middle_piece = board[middle_row][middle_col]

        if belongs_to_opponent(middle_piece, player):
            if board[end_row][end_col] == EMPTY:
                captures.append(
                    (end_row, end_col, middle_row, middle_col)
                )

    return captures


# Check if the player has any capture on the board
def player_has_capture(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                if get_capture_moves(board, row, col, player):
                    return True

    return False


# Get legal moves for one selected piece
def get_legal_moves(board, row, col, player):
    if not is_on_board(row, col):
        return []

    if not belongs_to_player(board[row][col], player):
        return []

    captures = get_capture_moves(board, row, col, player)

    if player_has_capture(board, player):
        return captures

    moves = []

    for end_row, end_col in get_simple_moves(board, row, col, player):
        moves.append((end_row, end_col, None, None))

    return moves


# Check whether the player has any legal move
def player_has_legal_move(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                if get_legal_moves(board, row, col, player):
                    return True

    return False


def count_pieces(board, player):
    count = 0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                count += 1

    return count


# Move a piece and remove a captured piece if needed
def make_move(board, start_row, start_col, move):
    end_row, end_col, captured_row, captured_col = move

    piece = board[start_row][start_col]

    board[end_row][end_col] = piece
    board[start_row][start_col] = EMPTY

    if captured_row is not None:
        board[captured_row][captured_col] = EMPTY

    promoted = promote_piece(board, end_row, end_col)

    return end_row, end_col, captured_row is not None, promoted


# Turn a normal piece into a king
def promote_piece(board, row, col):
    piece = board[row][col]

    if piece == RED and row == 0:
        board[row][col] = RED_KING
        return True

    if piece == BLACK and row == BOARD_SIZE - 1:
        board[row][col] = BLACK_KING
        return True

    return False


def switch_player(player):
    if player == "red":
        return "black"

    return "red"


def read_move():
    print("Enter move as: start_row start_col end_row end_col")
    print("Enter q to quit.")

    user_input = input("> ").strip()

    if user_input.lower() == "q":
        return "quit"

    move = user_input.split()

    if len(move) != 4:
        return None

    try:
        return [int(value) for value in move]
    except ValueError:
        return None


# Find a move that matches the user's coordinates
def find_move(legal_moves, end_row, end_col):
    for move in legal_moves:
        if move[0] == end_row and move[1] == end_col:
            return move

    return None


def main():
    board = create_board()
    current_player = "red"
    forced_piece = None

    print("Checkers")
    print("Rows and columns are numbered 0 through 7.")

    while True:
        # Check whether the current player has lost
        if count_pieces(board, current_player) == 0:
            winner = switch_player(current_player)
            print_board(board)
            print(winner.capitalize() + " wins!")
            break

        if not player_has_legal_move(board, current_player):
            winner = switch_player(current_player)
            print_board(board)
            print(winner.capitalize() + " wins!")
            break

        print_board(board)
        print(current_player.capitalize() + "'s turn")

        if forced_piece is not None:
            print(
                "Another jump is required with piece at",
                forced_piece[0],
                forced_piece[1]
            )
        elif player_has_capture(board, current_player):
            print("A capture is required.")

        move_input = read_move()

        if move_input == "quit":
            print("Game ended.")
            break

        if move_input is None:
            print("Invalid input.")
            continue

        start_row, start_col, end_row, end_col = move_input

        if not is_on_board(start_row, start_col):
            print("Invalid move.")
            continue

        if not is_on_board(end_row, end_col):
            print("Invalid move.")
            continue

        # During a multi-jump the same piece must move again
        if forced_piece is not None:
            if (start_row, start_col) != forced_piece:
                print("You must continue the jump with the same piece.")
                continue

            legal_moves = get_capture_moves(
                board,
                start_row,
                start_col,
                current_player
            )
        else:
            legal_moves = get_legal_moves(
                board,
                start_row,
                start_col,
                current_player
            )

        selected_move = find_move(
            legal_moves,
            end_row,
            end_col
        )

        if selected_move is None:
            print("Invalid move. Try again.")
            continue

        new_row, new_col, was_capture, promoted = make_move(
            board,
            start_row,
            start_col,
            selected_move
        )

        # Continue jumping if another capture is available
        if was_capture and not promoted:
            more_captures = get_capture_moves(
                board,
                new_row,
                new_col,
                current_player
            )

            if more_captures:
                forced_piece = (new_row, new_col)
                continue

        forced_piece = None
        current_player = switch_player(current_player)


if __name__ == "__main__":
    main()