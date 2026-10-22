from src.game import create_board, print_board

PIECES = {".", "r", "R", "b", "B"}

def parse_board(layout):
    rows = [line.split() for line in layout.strip().splitlines()]

    assert len(rows) == 8, "board must have 8 rows"

    for row_index, row in enumerate(rows):
        assert len(row) == 8, "row " + str(row_index) + " must have 8 squares"

        for col_index, piece in enumerate(row):
            assert piece in PIECES, "unknown piece " + piece

            if piece != "." and (row_index + col_index) % 2 == 0:
                raise ValueError(
                    "piece on light square at "
                    + str((row_index, col_index))
                )

    return [row[:] for row in rows]


# State 1: opening positions
OPENING = create_board()

# State 2: midgame
MIDGAME = parse_board("""
    . b . b . . . b
    b . . . b . b .
    . . . b . b . .
    . . b . . . . .
    . r . . . r . .
    r . r . . . r .
    . r . . . r . .
    r . . . r . . .
""")

# State 3: endgame
ENDGAME = parse_board("""
    . . . . . B . .
    . . . . . . . .
    . b . . . . . .
    . . b . . . . .
    . . . . . r . .
    r . . . . . . .
    . . . . . . . .
    . . R . . . . .
""")

# name -> (board, player to move)
FIXED_STATES = {
    "opening": (OPENING, "red"),
    "midgame": (MIDGAME, "red"),
    "endgame": (ENDGAME, "red"),
}


def get_fixed_states():
    return {
        name: ([row[:] for row in board], player)
        for name, (board, player) in FIXED_STATES.items()
    }


if __name__ == "__main__":
    from src.game import get_all_legal_turns, count_pieces

    for name, (board, player) in get_fixed_states().items():
        print(name.upper(), "-", player, "to move")
        print_board(board)
        print(
            "Red pieces:", count_pieces(board, "red"),
            "| Black pieces:", count_pieces(board, "black"),
            "| Legal turns:", len(get_all_legal_turns(board, player))
        )
        print()