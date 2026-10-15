from src.game import (
    create_board,
    copy_board,
    get_all_legal_moves,
    make_move_on_copy,
    count_pieces,
    promote_piece,
    get_winner,
    get_utility,
    EMPTY,
    RED,
    BLACK
)


def test_starting_board():
    board = create_board()

    print("Red pieces:", count_pieces(board, "red"))
    print("Black pieces:", count_pieces(board, "black"))
    print("Red legal moves:", len(get_all_legal_moves(board, "red")))
    print("Black legal moves:", len(get_all_legal_moves(board, "black")))


def test_board_copy():
    board = create_board()
    original = copy_board(board)

    moves = get_all_legal_moves(board, "red")
    start_row, start_col, move = moves[0]

    new_board = make_move_on_copy(
        board,
        start_row,
        start_col,
        move
    )

    print("Original board unchanged:", board == original)
    print("Copied board changed:", new_board != board)


def test_promotion():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    board[1][2] = RED
    board[0][3] = board[1][2]
    board[1][2] = EMPTY

    promote_piece(board, 0, 3)

    print("Promoted piece:", board[0][3])


def test_winner():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    board[0][1] = RED
    board[6][1] = BLACK

    print("Winner if red turn:", get_winner(board, "red"))
    print("Winner if black turn:", get_winner(board, "black"))
    print("Utility for black:", get_utility(board, "black", "red"))


test_starting_board()
print()

test_board_copy()
print()

test_promotion()
print()

test_winner()