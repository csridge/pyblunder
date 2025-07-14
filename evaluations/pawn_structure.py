import chess
from evaluations.pawn_structure_arr import arr_files, arr_front_span, arr_neighbor_files
from zobrist import compute_pawn_hash

def doubled_pawns(board:chess.Board, color: chess.Color):
    pawns = list(board.pieces(chess.PAWN, color))
    # Doubled pawns check
    doubled = 0
    for square in pawns:
        file = chess.square_file(square)
        pawns_of_file = arr_files[file] & board.pieces_mask(chess.PAWN, color)
        if pawns_of_file & (pawns_of_file - 1):
            """When a number n is a power of 2 (i.e only one bit is set), means the current file only has 1 pawn
            n & (n - 1) == 0.
            Therefore, if n & (n - 1) is non-zero, the current file has more than 1 pawn, 
            therefore they are doubled pawns."""
            doubled += 1
    return -5 * doubled

def isolated_pawns(board: chess.Board, color: chess.Color):
    pawns = list(board.pieces(chess.PAWN, color))
    isolated = 0
    for square in pawns:
        file = square & 7
        if (arr_neighbor_files[file] & board.pieces_mask(chess.PAWN, color)) == 0:
            """The bitwise AND gives the only square where a pawn and a neighbor file overlap.
            If the result is 0, no pawns are on the adjacent file, therefore the current pawn is isolated."""
            isolated += 1
    return -5 * isolated

def passed_pawns(board: chess.Board, color: chess.Color):
    pawns = list(board.pieces(chess.PAWN, color))
    enemy_pawns: chess.Bitboard = board.pieces_mask(chess.PAWN, not color)
    passed_score = 0
    for square in pawns:
        if (arr_front_span[color][square] & enemy_pawns) == 0:
            rank = square >> 3
            passed_score += 20 * (8 - rank) # The more close to promotion, the more score gained

    return passed_score

pawn_table: dict[int, int] = {}
def pawn_structure(board: chess.Board, color: chess.Color) -> int:
    key = compute_pawn_hash(board)
    if key in pawn_table:
        return pawn_table[key]
    
    total = 0
    total += doubled_pawns(board, color)
    total += isolated_pawns(board, color)
    total += passed_pawns(board, color)

    pawn_table[key] = total

    return total