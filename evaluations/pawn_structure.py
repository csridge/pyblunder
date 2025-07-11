import chess
pawn_table: dict[int, int] = {}

def pawn_hash(board: chess.Board) -> int:
    white_pawns = int(board.pieces(chess.PAWN, chess.WHITE))
    black_pawns = int(board.pieces(chess.PAWN, chess.BLACK))
    return hash((white_pawns, black_pawns, board.turn))  # optionally add en passant square

def pawn_structure(board: chess.Board, color: chess.Color) -> int:
    key = pawn_hash(board)
    if key in pawn_table:
        return pawn_table[key]
    
    total = 0

    # Doubled pawns check
    pawns = list(board.pieces(chess.PAWN, color))
    enemy_pawns = board.pieces(chess.PAWN, not color)

    file_counts = [0] * 8
    pawn_files = [[] for _ in range(8)]  # Track rank for passed pawn check

    for square in pawns:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        file_counts[file] += 1
        pawn_files[file].append(rank)

    doubled = sum(1 for count in file_counts if count > 1)
    total -= 5 * doubled

    # Isolated pawns check
    isolated = 0
    for file in range(8):
        if file_counts[file] == 0:
            continue
        left = file_counts[file - 1] if file > 0 else 0
        right = file_counts[file + 1] if file < 7 else 0
        if left == 0 and right == 0:
            isolated += file_counts[file]
    
    total -= 5 * isolated
    # Passed pawns check
    passed = 0

    for square in pawns:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        is_passed = True

        for adj_file in [file - 1, file, file + 1]:
            if not (0 <= adj_file <= 7):
                continue

            if color == chess.WHITE:
                for r in range(rank + 1, 8):
                    if chess.square(adj_file, r) in enemy_pawns:
                        is_passed = False
                        break
            else:
                for r in range(rank - 1, -1, -1):
                    if chess.square(adj_file, r) in enemy_pawns:
                        is_passed = False
                        break

            if not is_passed:
                break

        if is_passed:
            distance = 7 - rank if color == chess.WHITE else rank
            total += 10 * (7 - distance)

    return total