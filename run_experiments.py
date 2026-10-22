"""Track A experiments: Minimax vs Alpha-Beta on the fixed board states.

Run from the repo root:
    python -m experiments.run_experiments

Table 2A: same depth, every fixed state, both algorithms.
Table 2B: cutoff-depth study, every fixed state, depths 1 to MAX_STUDY_DEPTH.
Results are printed and saved as CSV files in results/.
"""

import csv
import os
import platform
import statistics
import sys

from fixed_states import get_fixed_states
from src.minimax import MinimaxAgent
from src.alphabeta import AlphaBetaAgent

COMPARISON_DEPTH = 3     # depth used for table 2A
MAX_STUDY_DEPTH = 3      # table 2B runs depths 1 .. MAX_STUDY_DEPTH
TIMING_REPEATS = 3       # each search is repeated; median time reported
RESULTS_DIR = "results"

ALGORITHMS = {
    "Minimax": MinimaxAgent,
    "Alpha-Beta": AlphaBetaAgent,
}


def format_turn(turn):
    if turn is None:
        return "none"

    return "->".join("(" + str(r) + "," + str(c) + ")" for r, c in turn)


def run_search(algorithm, board, player, depth):
    times = []
    turn = None
    metrics = None

    for _ in range(TIMING_REPEATS):
        agent = ALGORITHMS[algorithm](max_depth=depth)
        turn, metrics = agent.get_best_turn(board, player)
        times.append(metrics["decision_time"])

    return {
        "move": format_turn(turn),
        "value": round(metrics["eval_value"], 2) + 0.0,
        "nodes": metrics["nodes_visited"],
        "pruned": metrics["pruned_branches"],
        "time": statistics.median(times),
    }


def table_2a(states):
    rows = []

    for number, (name, (board, player)) in enumerate(states.items(), start=1):
        for algorithm in ALGORITHMS:
            result = run_search(algorithm, board, player, COMPARISON_DEPTH)
            rows.append({
                "State": "State " + str(number) + " (" + name + ")",
                "Algorithm": algorithm,
                "Depth": COMPARISON_DEPTH,
                "Chosen move": result["move"],
                "Value": result["value"],
                "Nodes evaluated": result["nodes"],
                "Pruned branches": result["pruned"],
                "Time (s)": round(result["time"], 4),
            })

    return rows


def table_2b(states):
    rows = []

    for number, (name, (board, player)) in enumerate(states.items(), start=1):
        for algorithm in ALGORITHMS:
            previous_move = None
            previous_nodes = None

            for depth in range(1, MAX_STUDY_DEPTH + 1):
                result = run_search(algorithm, board, player, depth)

                observation = []

                if previous_move is None:
                    observation.append("first depth tested")
                elif result["move"] != previous_move:
                    observation.append("move changed from depth " + str(depth - 1))
                else:
                    observation.append("same move as depth " + str(depth - 1))

                if previous_nodes:
                    growth = result["nodes"] / previous_nodes
                    observation.append("nodes x" + str(round(growth, 1)))

                rows.append({
                    "State": "State " + str(number) + " (" + name + ")",
                    "Algorithm": algorithm,
                    "Depth": depth,
                    "Chosen move": result["move"],
                    "Value": result["value"],
                    "Nodes": result["nodes"],
                    "Pruned": result["pruned"],
                    "Time (s)": round(result["time"], 4),
                    "Observation": "; ".join(observation),
                })

                previous_move = result["move"]
                previous_nodes = result["nodes"]

    return rows


def check_agreement(rows_2a):
    by_state = {}

    for row in rows_2a:
        by_state.setdefault(row["State"], []).append(row)

    all_agree = True

    for state, pair in by_state.items():
        if pair[0]["Chosen move"] != pair[1]["Chosen move"] or pair[0]["Value"] != pair[1]["Value"]:
            print("WARNING: agents disagree on " + state)
            all_agree = False

    if all_agree:
        print("Check: Minimax and Alpha-Beta chose the same move and value in every state.")


def print_table(title, rows):
    print()
    print(title)

    headers = list(rows[0].keys())
    widths = [
        max(len(header), max(len(str(row[header])) for row in rows))
        for header in headers
    ]

    print("  ".join(header.ljust(width) for header, width in zip(headers, widths)))
    print("  ".join("-" * width for width in widths))

    for row in rows:
        print("  ".join(str(row[header]).ljust(width) for header, width in zip(headers, widths)))


def save_csv(filename, rows):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)

    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("Saved " + path)


def print_controls():
    print("Experimental controls (table 1)")
    print("  Runtime: Python " + platform.python_version() + " on " + platform.platform())
    print("  Board: 8x8, standard checkers rules as implemented in src/game.py")
    print("  Search: fixed depth, no time limit, no randomness (no seed needed)")
    print("  Timing: median of " + str(TIMING_REPEATS) + " runs per search")


def main():
    states = get_fixed_states()

    print_controls()

    rows_2a = table_2a(states)
    print_table("Table 2A - Minimax vs Alpha-Beta (depth " + str(COMPARISON_DEPTH) + ")", rows_2a)
    check_agreement(rows_2a)

    rows_2b = table_2b(states)
    print_table("Table 2B - Cutoff-depth study", rows_2b)

    print()
    save_csv("table_2a_minimax_vs_alphabeta.csv", rows_2a)
    save_csv("table_2b_cutoff_depth.csv", rows_2b)


if __name__ == "__main__":
    sys.exit(main())