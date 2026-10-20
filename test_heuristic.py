from src.game import (
    create_board,
    EMPTY,
    RED,
    RED_KING,
    BLACK
)

from src.heuristic import evaluate_board


def empty_board():
    return [[EMPTY for _ in range(8)] for _ in range(8)]


def test_starting_board():
    board = create_board()

    red_score = evaluate_board(board, "red")
    black_score = evaluate_board(board, "black")

    print("Starting red score:", red_score)
    print("Starting black score:", black_score)

    assert abs(red_score) < 1
    assert abs(black_score) < 1

    print("Starting board heuristic test: PASS")


def test_material_advantage():
    board = empty_board()

    board[5][0] = RED
    board[5][2] = RED
    board[2][1] = BLACK

    red_score = evaluate_board(board, "red")
    black_score = evaluate_board(board, "black")

    print("Red material advantage score:", red_score)
    print("Black material disadvantage score:", black_score)

    assert red_score > 0
    assert black_score < 0

    print("Material advantage test: PASS")


def test_king_value():
    board = empty_board()

    board[4][1] = RED_KING
    board[3][2] = BLACK

    red_score = evaluate_board(board, "red")

    print("Red king vs black piece score:", red_score)

    assert red_score > 0

    print("King value test: PASS")


def test_opposite_perspectives():
    board = empty_board()

    board[5][0] = RED
    board[5][2] = RED_KING
    board[2][1] = BLACK

    red_score = evaluate_board(board, "red")
    black_score = evaluate_board(board, "black")

    print("Red perspective:", red_score)
    print("Black perspective:", black_score)

    assert red_score > 0
    assert black_score < 0

    print("Perspective test: PASS")


def run_tests():
    test_starting_board()
    print()

    test_material_advantage()
    print()

    test_king_value()
    print()

    test_opposite_perspectives()
    print()

    print("All heuristic tests passed.")


if __name__ == "__main__":
    run_tests()