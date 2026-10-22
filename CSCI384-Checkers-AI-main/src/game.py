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


def copy_board(board):
    return [row[:] for row in board]


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


# Find normal moves for one piece
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


# Find one-jump captures for a piece
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

        if not is_on_board(middle_row, middle_col):
            continue

        if not is_on_board(end_row, end_col):
            continue

        middle_piece = board[middle_row][middle_col]

        if belongs_to_opponent(middle_piece, player):
            if board[end_row][end_col] == EMPTY:
                captures.append(
                    (end_row, end_col, middle_row, middle_col)
                )

    return captures


def player_has_capture(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                if get_capture_moves(board, row, col, player):
                    return True

    return False


# Legal one-step moves used by the CLI
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


def get_all_legal_moves(board, player):
    all_moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                moves = get_legal_moves(board, row, col, player)

                for move in moves:
                    all_moves.append((row, col, move))

    return all_moves


def count_pieces(board, player):
    count = 0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                count += 1

    return count


def promote_piece(board, row, col):
    piece = board[row][col]

    if piece == RED and row == 0:
        board[row][col] = RED_KING
        return True

    if piece == BLACK and row == BOARD_SIZE - 1:
        board[row][col] = BLACK_KING
        return True

    return False


# Apply one move
def make_move(board, start_row, start_col, move):
    end_row, end_col, captured_row, captured_col = move

    piece = board[start_row][start_col]

    board[end_row][end_col] = piece
    board[start_row][start_col] = EMPTY

    if captured_row is not None:
        board[captured_row][captured_col] = EMPTY

    promoted = promote_piece(board, end_row, end_col)

    return end_row, end_col, captured_row is not None, promoted


def make_move_on_copy(board, start_row, start_col, move):
    new_board = copy_board(board)

    make_move(
        new_board,
        start_row,
        start_col,
        move
    )

    return new_board


# Find every complete capture sequence for one piece
def get_capture_sequences(board, row, col, player, path=None):
    if path is None:
        path = [(row, col)]

    captures = get_capture_moves(board, row, col, player)

    if not captures:
        if len(path) > 1:
            return [path]

        return []

    sequences = []

    for move in captures:
        new_board = copy_board(board)

        new_row, new_col, was_capture, promoted = make_move(
            new_board,
            row,
            col,
            move
        )

        new_path = path + [(new_row, new_col)]

        # A piece that becomes a king ends its turn
        if promoted:
            sequences.append(new_path)
            continue

        more_sequences = get_capture_sequences(
            new_board,
            new_row,
            new_col,
            player,
            new_path
        )

        if more_sequences:
            sequences.extend(more_sequences)
        else:
            sequences.append(new_path)

    return sequences


# Get every complete legal turn for the AI
def get_all_legal_turns(board, player):
    turns = []

    if player_has_capture(board, player):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if belongs_to_player(board[row][col], player):
                    sequences = get_capture_sequences(
                        board,
                        row,
                        col,
                        player
                    )

                    turns.extend(sequences)

        return turns

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if belongs_to_player(board[row][col], player):
                simple_moves = get_simple_moves(
                    board,
                    row,
                    col,
                    player
                )

                for end_row, end_col in simple_moves:
                    turns.append(
                        [(row, col), (end_row, end_col)]
                    )

    return turns


# Apply an entire AI turn to a copied board
def apply_turn(board, turn):
    new_board = copy_board(board)

    if len(turn) < 2:
        return new_board

    current_row, current_col = turn[0]

    for next_row, next_col in turn[1:]:
        row_change = next_row - current_row
        col_change = next_col - current_col

        captured_row = None
        captured_col = None

        if abs(row_change) == 2 and abs(col_change) == 2:
            captured_row = (current_row + next_row) // 2
            captured_col = (current_col + next_col) // 2

        move = (
            next_row,
            next_col,
            captured_row,
            captured_col
        )

        new_row, new_col, was_capture, promoted = make_move(
            new_board,
            current_row,
            current_col,
            move
        )

        current_row = new_row
        current_col = new_col

        if promoted:
            break

    return new_board


def player_has_legal_move(board, player):
    return len(get_all_legal_turns(board, player)) > 0


def switch_player(player):
    if player == "red":
        return "black"

    return "red"


def get_winner(board, current_player):
    if count_pieces(board, "red") == 0:
        return "black"

    if count_pieces(board, "black") == 0:
        return "red"

    if not player_has_legal_move(board, current_player):
        return switch_player(current_player)

    return None


def get_utility(board, max_player, current_player):
    winner = get_winner(board, current_player)

    if winner is None:
        return 0

    if winner == max_player:
        return 1

    return -1


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
        winner = get_winner(board, current_player)

        if winner is not None:
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