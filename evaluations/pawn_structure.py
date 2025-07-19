import chess
from evaluations.pawn_structure_arr import arr_files, arr_front_span, arr_neighbor_files
import random
# import time

random.seed(3333)
pawn_zobrist_table = [[random.getrandbits(64) for _ in range(64)] for _ in range(2)]

def compute_pawn_hash(board: chess.Board) -> int:
    h = 0
    for square, piece in board.piece_map().items():
        if piece and piece.piece_type == chess.PAWN:
            color: bool = piece.color
            h ^= pawn_zobrist_table[color][square] # chess.Color is a bool, therefore it's also an int
    return h

def doubled_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns: chess.SquareSet = board.pieces(chess.PAWN, color)
    pawn_bb = board.pieces_mask(chess.PAWN, color)
    doubled = 0

    for sq in pawns:
        file = sq & 7
        pawns_on_file = arr_files[file] & pawn_bb
        if pawns_on_file & (pawns_on_file - 1):
            doubled += 1
    
    return doubled

def isolated_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns: chess.SquareSet = board.pieces(chess.PAWN, color)
    pawn_bb = board.pieces_mask(chess.PAWN, color)
    isolated = 0

    for sq in pawns:
        file = sq & 7
        if (arr_neighbor_files[file] & pawn_bb) == 0:
            isolated += 1
    return isolated


def passed_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns = board.pieces_mask(chess.PAWN, color)
    enemy_pawns = board.pieces_mask(chess.PAWN, not color)
    passed = 0
    bb = pawns
    while bb:
        r = bb & -bb
        square = r.bit_length() - 1
        bb ^= r

        if not arr_front_span[color][square] & enemy_pawns:
            passed += 1
    return passed


pawn_table: dict[int, int] = {}
def pawn_structure(board: chess.Board) -> int:
    key = compute_pawn_hash(board)
    if key in pawn_table:
        return pawn_table[key]
    
    structure_score: int = (
        -5 * (doubled_pawns(board, chess.WHITE) - doubled_pawns(board, chess.BLACK))
        - 5  * (isolated_pawns(board, chess.WHITE) - isolated_pawns(board, chess.BLACK))
        + 20 * (passed_pawns(board, chess.WHITE) - passed_pawns(board, chess.BLACK))
    )

    pawn_table[key] = structure_score

    return structure_score