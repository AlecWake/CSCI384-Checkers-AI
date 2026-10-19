import time
from src.game import (
    get_all_legal_turns,
    apply_turn,
    get_winner,
    switch_player
)

def simple_piece_count_heuristic(board, player):
    # Base heuristic checking piece balance
    score = 0
    opponent = switch_player(player)
    for row in board:
        for cell in row:
            if cell.lower() == player[0]:
                score += 2 if cell.isupper() else 1
            elif cell.lower() == opponent[0]:
                score -= 2 if cell.isupper() else 1
    return score

class MinimaxAgent:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.nodes_visited = 0

    def minimax(self, board, depth, is_maximizing, current_player, max_player):
        self.nodes_visited += 1

        # Terminal state check for winner
        winner = get_winner(board, current_player)
        if winner is not None:
            if winner == max_player:
                return 1000 + depth, None
            else:
                return -1000 - depth, None

        # Depth limit cutoff
        if depth == 0:
            return simple_piece_count_heuristic(board, max_player), None

        legal_turns = get_all_legal_turns(board, current_player)
        # Terminal state check for no legal moves (stalemate/loss)
        if not legal_turns:
            if current_player == max_player:
                return -1000 - depth, None
            else:
                return 1000 + depth, None

        best_turn = legal_turns[0]

        if is_maximizing:
            max_eval = float('-inf')
            for turn in legal_turns:
                next_board = apply_turn(board, turn)
                eval_score, _ = self.minimax(
                    next_board,
                    depth - 1,
                    False,
                    switch_player(current_player),
                    max_player
                )
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_turn = turn
            return max_eval, best_turn
        else:
            min_eval = float('inf')
            for turn in legal_turns:
                next_board = apply_turn(board, turn)
                eval_score, _ = self.minimax(
                    next_board,
                    depth - 1,
                    True,
                    switch_player(current_player),
                    max_player
                )
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_turn = turn
            return min_eval, best_turn

    def get_best_turn(self, board, current_player):
        # Entry point called by main to get the best move and metrics
        self.nodes_visited = 0
        start_time = time.time()

        eval_score, best_turn = self.minimax(
            board,
            self.max_depth,
            True,
            current_player,
            current_player
        )

        elapsed_time = time.time() - start_time
        metrics = {
            "nodes_visited": self.nodes_visited,
            "pruned_branches": 0,
            "decision_time": round(elapsed_time, 4),
            "eval_value": eval_score
        }
        return best_turn, metrics

if __name__ == "__main__":
    from src.game import create_board

    board = create_board()
    agent = MinimaxAgent(max_depth=3)
    turn, stats = agent.get_best_turn(board, "black")

    print("Minimax Testing:")
    print("Chosen Turn:", turn)
    print("Metrics:", stats)