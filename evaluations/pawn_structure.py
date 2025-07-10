import chess

def doubled_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns = board.pieces(chess.PAWN, color)
    file_counts = [0] * 8 # Track the number of pawns on each file

    for square in pawns:
        file = chess.square_file(square)
        file_counts[file] += 1

    doubled = 0
    for count in file_counts:
        if count > 1: # More than 1 pawn on a file
            doubled += 1
    return -(6 * doubled) # Returns penalty based on the number of doubled files

def isolated_pawns(board: chess.Board, color: bool) -> int:
    pawns = board.pieces(chess.PAWN, color)
    file_counts = [0] * 8

    for square in pawns:
        file = chess.square_file(square)
        file_counts[file] += 1

    isolated = 0
    for square in pawns:
        file = chess.square_file(square)
        left = file_counts[file - 1] if file > 0 else 0 # If file = 0, then left is out of bound
        right = file_counts[file + 1] if file < 7 else 0 # If file = 7, then right is out of bound
        if left == 0 and right == 0: # No friendly pawns around -> isolated
            isolated += 1

    return -(5 * isolated)

def passed_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns = board.pieces(chess.PAWN, color)
    enemy_pawns = board.pieces(chess.PAWN, not color)

    passed = 0 # Amount of passed pawns

    for square in pawns:
        file = chess.square_file(square)
        rank = chess.square_rank(square)

        is_passed = True # assume there is a passed pawn

        for adj_file in [file - 1, file, file + 1]: # check for adjacent files
            if not (0 <= adj_file <= 7):
                continue

            # Loop though ranks in front(depends on color)
            if color == chess.WHITE:
                for r in range(rank + 1, 8): # ahead of white pawn
                    sq = chess.square(adj_file, r)
                    if sq in enemy_pawns:
                        is_passed = False
                        break
            else:
                for r in range(rank - 1, -1, -1): # ahead of black pawn
                    sq = chess.square(adj_file, r)
                    if sq in enemy_pawns:
                        is_passed = False
                        break

            if not is_passed:
                break

        if is_passed:
            passed += 1

    return 15 * passed

def pawn_structure(board: chess.Board, color: chess.Color) -> int:
    return doubled_pawns(board, color) + isolated_pawns(board, color) + passed_pawns(board, color)