import chess
from pst import pst
from evaluations.pawn_structure import pawn_structure
pieces_val = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 69420 # must be this number
}

def evaluate(board: chess.Board):
    if board.is_checkmate():
        return -20000
    white: float = 0
    black: float = 0

    white_pawn_score = pawn_structure(board, chess.WHITE)
    black_pawn_score = pawn_structure(board, chess.BLACK)
    pawn_structure_score = white_pawn_score - black_pawn_score
        
    for square in chess.SQUARES:
        piece: chess.Piece = board.piece_at(square)
        if not piece:
            continue
        index = square if piece.color == chess.BLACK else chess.square_mirror(square)
        val = pieces_val[piece.piece_type] + pst[piece.piece_type][index] / 100
        if piece.color == chess.WHITE:
            white += val
        else:
            black += val
    
    return (white - black) + pawn_structure_score