from src.game import (
    RED,
    RED_KING,
    BLACK,
    BLACK_KING,
    get_all_legal_turns
)


def evaluate_board(board, player):
    score = 0

    if player == "red":
        opponent = "black"
        player_piece = RED
        player_king = RED_KING
        opponent_piece = BLACK
        opponent_king = BLACK_KING
    else:
        opponent = "red"
        player_piece = BLACK
        player_king = BLACK_KING
        opponent_piece = RED
        opponent_king = RED_KING

    # Material score
    for row in board:
        for piece in row:
            if piece == player_piece:
                score += 3
            elif piece == player_king:
                score += 5
            elif piece == opponent_piece:
                score -= 3
            elif piece == opponent_king:
                score -= 5

    # Mobility score
    player_moves = len(get_all_legal_turns(board, player))
    opponent_moves = len(get_all_legal_turns(board, opponent))

    score += (player_moves - opponent_moves) * 0.2

    # Small advancement bonus for regular pieces
    for row_index in range(8):
        for col_index in range(8):
            piece = board[row_index][col_index]

            if piece == RED:
                value = (7 - row_index) * 0.1

                if player == "red":
                    score += value
                else:
                    score -= value

            elif piece == BLACK:
                value = row_index * 0.1

                if player == "black":
                    score += value
                else:
                    score -= value

    return round(score, 2)