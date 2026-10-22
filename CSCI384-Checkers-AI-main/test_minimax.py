from src.game import (
    create_board,
    get_all_legal_turns,
    EMPTY,
    RED,
    RED_KING,
    BLACK
)
from src.minimax import MinimaxAgent


def empty_board():
    return [[EMPTY for _ in range(8)] for _ in range(8)]


def test_starting_board():
    board = create_board()
    agent = MinimaxAgent(max_depth=3)
    red_turn, red_stats = agent.get_best_turn(board, "red")
    black_turn, black_stats = agent.get_best_turn(board, "black")
    print("Starting board - Red decision:", red_turn, "Stats:", red_stats)
    print("Starting board - Black decision:", black_turn, "Stats:", black_stats)
    assert abs(red_stats["eval_value"]) < 3
    assert abs(black_stats["eval_value"]) < 3
    assert red_stats["nodes_visited"] > 0
    assert red_stats["pruned_branches"] == 0
    assert black_stats["pruned_branches"] == 0
    print("Starting board Minimax test: PASS")


def test_returns_legal_turn():
    board = create_board()
    agent = MinimaxAgent(max_depth=3)
    for player in ("red", "black"):
        turn, _ = agent.get_best_turn(board, player)
        print(player.capitalize(), "chose:", turn)
        assert turn in get_all_legal_turns(board, player)
    print("Legal turn test: PASS")


def test_takes_forced_capture():
    board = empty_board()
    board[4][3] = RED
    board[3][2] = BLACK
    board[0][7] = BLACK
    agent = MinimaxAgent(max_depth=3)
    turn, _ = agent.get_best_turn(board, "red")
    print("Forced capture turn:", turn)
    assert turn == [(4, 3), (2, 1)]
    print("Forced capture test: PASS")


def test_finds_winning_capture():
    board = empty_board()
    board[4][3] = RED
    board[3][2] = BLACK
    agent = MinimaxAgent(max_depth=2)
    turn, stats = agent.get_best_turn(board, "red")
    print("Winning capture turn:", turn, "eval:", stats["eval_value"])
    assert turn == [(4, 3), (2, 1)]
    assert stats["eval_value"] >= 1000
    print("Winning capture test: PASS")


def test_detects_loss_with_no_moves():
    board = empty_board()
    board[0][1] = RED
    board[7][6] = BLACK
    agent = MinimaxAgent(max_depth=3)
    turn, stats = agent.get_best_turn(board, "red")
    print("No legal moves eval:", stats["eval_value"])
    assert turn is None
    assert stats["eval_value"] <= -1000
    print("No legal moves test: PASS")


def test_material_advantage():
    board = empty_board()
    board[5][0] = RED
    board[5][2] = RED
    board[2][1] = BLACK
    agent = MinimaxAgent(max_depth=3)
    _, red_stats = agent.get_best_turn(board, "red")
    _, black_stats = agent.get_best_turn(board, "black")
    print("Red material advantage eval:", red_stats["eval_value"])
    print("Black material disadvantage eval:", black_stats["eval_value"])
    assert red_stats["eval_value"] > 0
    assert black_stats["eval_value"] < 0
    print("Material advantage test: PASS")


def test_opposite_perspectives():
    board = empty_board()
    board[5][0] = RED
    board[5][2] = RED_KING
    board[2][1] = BLACK
    agent = MinimaxAgent(max_depth=3)
    _, red_stats = agent.get_best_turn(board, "red")
    _, black_stats = agent.get_best_turn(board, "black")
    print("Red perspective eval:", red_stats["eval_value"])
    print("Black perspective eval:", black_stats["eval_value"])
    assert red_stats["eval_value"] > 0
    assert black_stats["eval_value"] < 0
    print("Perspective test: PASS")


def test_deeper_search_visits_more_nodes():
    board = create_board()
    shallow = MinimaxAgent(max_depth=2)
    deep = MinimaxAgent(max_depth=3)
    _, shallow_stats = shallow.get_best_turn(board, "red")
    _, deep_stats = deep.get_best_turn(board, "red")
    print("Depth 2 nodes:", shallow_stats["nodes_visited"])
    print("Depth 3 nodes:", deep_stats["nodes_visited"])
    assert deep_stats["nodes_visited"] > shallow_stats["nodes_visited"]
    print("Search depth test: PASS")


def test_deterministic():
    board = create_board()
    first_turn, first_stats = MinimaxAgent(max_depth=3).get_best_turn(board, "red")
    second_turn, second_stats = MinimaxAgent(max_depth=3).get_best_turn(board, "red")
    assert first_turn == second_turn
    assert first_stats["eval_value"] == second_stats["eval_value"]
    assert first_stats["nodes_visited"] == second_stats["nodes_visited"]
    print("Deterministic test: PASS")


def test_does_not_modify_board():
    board = create_board()
    snapshot = [row[:] for row in board]
    MinimaxAgent(max_depth=3).get_best_turn(board, "red")
    assert board == snapshot
    print("Board unchanged test: PASS")

def run_tests():
    test_starting_board()
    print()
    test_returns_legal_turn()
    print()
    test_takes_forced_capture()
    print()
    test_finds_winning_capture()
    print()
    test_detects_loss_with_no_moves()
    print()
    test_material_advantage()
    print()
    test_opposite_perspectives()
    print()
    test_deeper_search_visits_more_nodes()
    print()
    test_deterministic()
    print()
    test_does_not_modify_board()
    print()
    print("All Minimax agent tests passed.")


if __name__ == "__main__":
    run_tests()