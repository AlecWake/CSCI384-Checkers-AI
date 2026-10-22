from src.game import (
    create_board,
    EMPTY,
    RED,
    RED_KING,
    BLACK
)
from src.alphabeta import AlphaBetaAgent

def empty_board():
    return [[EMPTY for _ in range(8)] for _ in range(8)]

def test_starting_board():
    board = create_board()
    agent = AlphaBetaAgent(max_depth=3)
    red_turn, red_stats = agent.get_best_turn(board, "red")
    black_turn, black_stats = agent.get_best_turn(board, "black")
    print("Starting board - Red decision:", red_turn, "Stats:", red_stats)
    print("Starting board - Black decision:", black_turn, "Stats:", black_stats)
    assert abs(red_stats["eval_value"]) < 3
    assert abs(black_stats["eval_value"]) < 3
    assert red_stats["nodes_visited"] > 0
    assert red_stats["pruned_branches"] > 0
    print("Starting board Alpha-Beta test: PASS")

def test_material_advantage():
    board = empty_board()
    board[5][0] = RED
    board[5][2] = RED
    board[2][1] = BLACK
    agent = AlphaBetaAgent(max_depth=3)
    _, red_stats = agent.get_best_turn(board, "red")
    _, black_stats = agent.get_best_turn(board, "black")
    print("Red material advantage eval:", red_stats["eval_value"])
    print("Black material disadvantage eval:", black_stats["eval_value"])
    assert red_stats["eval_value"] > 0
    assert black_stats["eval_value"] < 0
    print("Material advantage test: PASS")

def test_king_value():
    board = empty_board()
    board[4][1] = RED_KING
    board[3][2] = BLACK
    agent = AlphaBetaAgent(max_depth=3)
    _, red_stats = agent.get_best_turn(board, "red")
    print("Red king vs black piece eval:", red_stats["eval_value"])
    assert red_stats["eval_value"] > 0
    print("King value test: PASS")

def test_opposite_perspectives():
    board = empty_board()
    board[5][0] = RED
    board[5][2] = RED_KING
    board[2][1] = BLACK
    agent = AlphaBetaAgent(max_depth=3)
    _, red_stats = agent.get_best_turn(board, "red")
    _, black_stats = agent.get_best_turn(board, "black")
    print("Red perspective eval:", red_stats["eval_value"])
    print("Black perspective eval:", black_stats["eval_value"])
    assert red_stats["eval_value"] > 0
    assert black_stats["eval_value"] < 0
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
    print("All Alpha-Beta agent board state tests passed.")

if __name__ == "__main__":
    run_tests()