import chess
from pst import pst
from evaluations.pawn_structure import pawn_structure
base_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 69420 # must be this number
}
pieces_values = {chess.WHITE: base_values, chess.BLACK: base_values}

def evaluate(board: chess.Board):
    if board.is_checkmate():
        return -20000
    
    white: int = 0
    black: int = 0
    score = {chess.WHITE: 0, chess.BLACK: 0}
    pieces: dict[chess.Square, chess.Piece] = board.piece_map()

    white_pawn_score: int = pawn_structure(board, chess.WHITE)
    black_pawn_score: int = pawn_structure(board, chess.BLACK)
    pawn_structure_score = white_pawn_score - black_pawn_score
        
    for square, piece in pieces.items():
        color = piece.color
        piecetype = piece.piece_type
        index = square if color == chess.WHITE else square ^ 0x38  # vertically flip a square.
                                                                   # being a bit obscure, fun isnt it?
        score[color] += pieces_values[color][piecetype] + pst[piecetype][index]
    white, black = score[chess.WHITE], score[chess.BLACK]

    return (white - black) + pawn_structure_score