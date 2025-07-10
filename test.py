import chess
move = chess.Move.from_uci("e2e4")
print(move.from_square)  # → 12 (which is e2)
print(move.to_square)    # → 28 (which is e4)

