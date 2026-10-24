import time
from src.heuristic import evaluate_board
from src.game import (
    get_all_legal_turns,
    apply_turn,
    get_winner,
    switch_player
)


class AlphaBetaAgent:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.nodes_visited = 0
        self.terminal_states = 0
        self.cutoff_states = 0
        self.pruned_branches = 0

    def alphabeta(
        self,
        board,
        depth,
        alpha,
        beta,
        is_maximizing,
        current_player,
        max_player
    ):
        self.nodes_visited += 1

        # Terminal state check
        winner = get_winner(board, current_player)

        if winner is not None:
            self.terminal_states += 1

            if winner == max_player:
                return 1000 + depth, None
            else:
                return -1000 - depth, None

        # Depth limit cutoff
        if depth == 0:
            self.cutoff_states += 1
            return evaluate_board(board, max_player), None

        legal_turns = get_all_legal_turns(board, current_player)

        # Backup terminal check in case no legal turns exist
        if not legal_turns:
            self.terminal_states += 1

            if current_player == max_player:
                return -1000 - depth, None
            else:
                return 1000 + depth, None

        best_turn = legal_turns[0]

        if is_maximizing:
            max_eval = float("-inf")

            for turn in legal_turns:
                next_board = apply_turn(board, turn)

                eval_score, _ = self.alphabeta(
                    next_board,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    switch_player(current_player),
                    max_player
                )

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_turn = turn

                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    self.pruned_branches += 1
                    break

            return max_eval, best_turn

        else:
            min_eval = float("inf")

            for turn in legal_turns:
                next_board = apply_turn(board, turn)

                eval_score, _ = self.alphabeta(
                    next_board,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                    switch_player(current_player),
                    max_player
                )

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_turn = turn

                beta = min(beta, eval_score)

                if beta <= alpha:
                    self.pruned_branches += 1
                    break

            return min_eval, best_turn

    def get_best_turn(self, board, current_player):
        # Reset metrics for each search
        self.nodes_visited = 0
        self.terminal_states = 0
        self.cutoff_states = 0
        self.pruned_branches = 0

        start_time = time.time()

        eval_score, best_turn = self.alphabeta(
            board,
            self.max_depth,
            float("-inf"),
            float("inf"),
            True,
            current_player,
            current_player
        )

        elapsed_time = time.time() - start_time

        metrics = {
            "nodes_visited": self.nodes_visited,
            "terminal_states": self.terminal_states,
            "cutoff_states": self.cutoff_states,
            "pruned_branches": self.pruned_branches,
            "decision_time": round(elapsed_time, 4),
            "eval_value": eval_score
        }

        return best_turn, metrics


if __name__ == "__main__":
    from src.game import create_board

    board = create_board()
    agent = AlphaBetaAgent(max_depth=3)

    turn, stats = agent.get_best_turn(board, "black")

    print("Alpha-Beta Testing:")
    print("Chosen Turn:", turn)
    print("Metrics:", stats)