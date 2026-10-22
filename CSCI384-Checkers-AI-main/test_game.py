from src.game import (
    create_board,
    copy_board,
    get_all_legal_moves,
    get_all_legal_turns,
    apply_turn,
    count_pieces,
    promote_piece,
    get_winner,
    get_utility,
    EMPTY,
    RED,
    RED_KING,
    BLACK
)


def empty_board():
    return [[EMPTY for _ in range(8)] for _ in range(8)]


def test_starting_board():
    board = create_board()

    assert count_pieces(board, "red") == 12
    assert count_pieces(board, "black") == 12

    assert len(get_all_legal_moves(board, "red")) == 7
    assert len(get_all_legal_moves(board, "black")) == 7

    print("Starting board test: PASS")


def test_board_copy():
    board = create_board()
    original = copy_board(board)

    turns = get_all_legal_turns(board, "red")
    new_board = apply_turn(board, turns[0])

    assert board == original
    assert new_board != board

    print("Board copy test: PASS")


def test_promotion():
    board = empty_board()

    board[1][2] = RED
    board[0][3] = board[1][2]
    board[1][2] = EMPTY

    promote_piece(board, 0, 3)

    assert board[0][3] == RED_KING

    print("Promotion test: PASS")


def test_winner():
    board = empty_board()

    board[0][1] = RED
    board[6][1] = BLACK

    assert get_winner(board, "red") == "black"
    assert get_winner(board, "black") is None
    assert get_utility(board, "black", "red") == 1

    print("Winner test: PASS")


def test_forced_capture():
    board = empty_board()

    board[5][0] = RED
    board[5][4] = RED
    board[4][1] = BLACK

    turns = get_all_legal_turns(board, "red")

    assert len(turns) == 1
    assert turns[0] == [(5, 0), (3, 2)]

    print("Forced capture test: PASS")


def test_multi_jump():
    board = empty_board()

    board[5][0] = RED
    board[4][1] = BLACK
    board[2][3] = BLACK

    turns = get_all_legal_turns(board, "red")

    expected_turn = [
        (5, 0),
        (3, 2),
        (1, 4)
    ]

    assert expected_turn in turns

    new_board = apply_turn(board, expected_turn)

    assert new_board[1][4] == RED
    assert new_board[4][1] == EMPTY
    assert new_board[2][3] == EMPTY
    assert board[5][0] == RED

    print("Multi-jump test: PASS")


def test_king_backward_move():
    board = empty_board()

    board[3][2] = RED_KING

    turns = get_all_legal_turns(board, "red")

    assert [(3, 2), (4, 1)] in turns
    assert [(3, 2), (4, 3)] in turns
    assert [(3, 2), (2, 1)] in turns
    assert [(3, 2), (2, 3)] in turns

    print("King movement test: PASS")


def test_promotion_ends_jump():
    board = empty_board()

    board[2][1] = RED
    board[1][2] = BLACK
    board[1][4] = BLACK

    turns = get_all_legal_turns(board, "red")

    assert [(2, 1), (0, 3)] in turns

    new_board = apply_turn(
        board,
        [(2, 1), (0, 3)]
    )

    assert new_board[0][3] == RED_KING
    assert new_board[1][2] == EMPTY
    assert new_board[1][4] == BLACK

    print("Promotion capture test: PASS")


def run_tests():
    test_starting_board()
    test_board_copy()
    test_promotion()
    test_winner()
    test_forced_capture()
    test_multi_jump()
    test_king_backward_move()
    test_promotion_ends_jump()

    print()
    print("All tests passed.")


if __name__ == "__main__":
    run_tests()