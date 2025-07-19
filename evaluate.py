import chess
from evaluations.pawn_structure import pawn_structure
pst_king_midgame = [
    -90, -100, -100, -120, -120, -100, -100, -90,
    -90, -100, -100, -120, -120, -100, -100, -90,
    -90, -100, -100, -120, -120, -100, -100, -90,
    -90, -100, -100, -120, -120, -100, -100, -90,
    -60, -80, -80, -100, -100, -80, -80, -60,
    -30, -50, -60, -60, -60, -60, -50, -30,
     -5,  -5, -45, -60, -60, -30,  -5,  -5,
    +80, +100, +30, -15,   0, +30, +100, +80
]
    
pst_king_endgame = [
-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50
]

# Shout out to Chess Programming Wiki for piece-square tables!!!
MIDGAME_PST = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 
                 5, 10, 10, -20, -20, 10, 10, 5, 
                 5, -5, -10, 0, 0, -10, -5, 5, 
                 0, 0, 0, 20, 20, 0, 0, 0, 
                 5, 5, 10, 25, 25, 10, 5, 5, 
                 10, 10, 20, 30, 30, 20, 10, 10, 
                 50, 50, 50, 50, 50, 50, 50, 50, 
                 0, 0, 0, 0, 0, 0, 0, 0],
    chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50, 
                   -40, -20, 0, 5, 5, 0, -20, -40,
                    -30, 5, 10, 15, 15, 10, 5, -30, 
                    -30, 0, 15, 20, 20, 15, 0, -30, 
                    -30, 5, 15, 20, 20, 15, 5, -30, 
                    -30, 0, 10, 15, 15, 10, 0, -30, 
                    -40, -20, 0, 0, 0, 0, -20, -40, 
                    -50, -40, -30, -30, -30, -30, -40, -50],

    chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20, 
                   -10, 5, 0, 0, 0, 0, 5, -10, 
                   -10, 10, 10, 10, 10, 10, 10, -10, 
                   -10, 0, 10, 10, 10, 10, 0, -10, 
                   -10, 5, 5, 10, 10, 5, 5, -10, 
                   -10, 0, 5, 10, 10, 5, 0, -10, 
                   -10, 0, 0, 0, 0, 0, 0, -10, 
                   -20, -10, -10, -10, -10, -10, -10, -20],

    chess.ROOK: [0, 0, 0, 5, 5, 0, 0, 0, 
                 -5, 0, 0, 0, 0, 0, 0, -5, 
                 -5, 0, 0, 0, 0, 0, 0, -5, 
                 -5, 0, 0, 0, 0, 0, 0, -5, 
                 -5, 0, 0, 0, 0, 0, 0, -5, 
                 -5, 0, 0, 0, 0, 0, 0, -5, 
                 5, 10, 10, 10, 10, 10, 10, 
                 5, 0, 0, 0, 0, 0, 0, 0, 0],

    chess.QUEEN: [-20, -10, -10, -5, -5, -10, -10, -20,
                  -10, 0, 5, 0, 0, 0, 0, -10, 
                  -10, 5, 5, 5, 5, 5, 0, -10, 
                  0, 0, 5, 5, 5, 5, 0, -5, 
                  -5, 0, 5, 5, 5, 5, 0, -5, 
                  -10, 0, 5, 5, 5, 5, 0, -10, 
                  -10, 0, 0, 0, 0, 0, 0, -10, 
                  -20, -10, -10, -5, -5, -10, -10, -20],

    chess.KING: [20, 40, 0, -5, -5, 0, 40, 20,
                 10, 10, -25,  -25, -25, -25, 10, 10, 
                -20, -30, -30, -40, -40, -30, -30, -20, 
                -30, -40, -40, -50, -50, -40, -40, -30, 
                -40, -50, -50, -60, -60, -50, -50, -40, 
                -40, -50, -50, -60, -60, -50, -50, -40,
                -40, -50, -50, -60, -60, -50, -50, -40,
                -40, -50, -50, -60, -60, -50, -50, -40,]
}
ENDGAME_PST = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 
                 13, 8, 8, 10, 13, 0, 2, -7, 
                 4, 7, -6, 1, 0, -5, -1, -8, 
                 13, 9, -3, -7, -7, -8, 3, -1, 
                 32, 24, 13, 5, -2, 4, 17, 17, 
                 94, 100, 85, 67, 56, 53, 82, 84, 
                 178, 173, 158, 134, 147, 132, 165, 187, 
                 0, 0, 0, 0, 0, 0, 0, 0],

    chess.KNIGHT: [-29, -51, -23, -15, -22, -18, -50, -64, 
                   -42, -20, -10, -5, -2, -20, -23, -44, 
                   -23, -3, -1, 15, 10, -3, -20, -22, 
                   -18, -6, 16, 25, 16, 17, 4, -18, 
                   -17, 3, 22, 22, 22, 11, 8, -18, 
                   -24, -20, 10, 9, -1, -9, -19, -41, 
                   -25, -8, -25, -2, -9, -25, -24, -52, 
                   -58, -38, -13, -28, -31, -27, -63, -99],

    chess.BISHOP: [-23, -9, -23, -5, -9, -16, -5, -17, 
                   -14, -18, -7, -1, 4, -9, -15, -27, 
                   -12, -3, 8, 10, 13, 3, -7, -15, 
                   -6, 3, 13, 19, 7, 10, -3, -9, 
                   -3, 9, 12, 9, 14, 10, 3, 2, 
                   2, -8, 0, -1, -2, 6, 0, 4, 
                   -8, -4, 7, -12, -3, -13, -4, -14, 
                   -14, -21, -11, -8, -7, -9, -17, -24],
    
    chess.ROOK: [-9, 2, 3, -1, -5, -13, 4, -20, 
                 -6, -6, 0, 2, -9, -9, -11, -3, 
                 -4, 0, -5, -1, -7, -12, -8, -16, 
                 3, 5, 8, 4, -5, -6, -8, -11, 
                 4, 3, 13, 1, 2, 1, -1, 2, 
                 7, 7, 7, 5, 4, -3, -5, -3, 
                 11, 13, 13, 11, -3, 3, 8, 3,
                 13, 10, 18, 15, 12, 12, 8, 5],
    
    chess.QUEEN: [-33, -28, -22, -43, -5, -32, -20, -41, 
                  -22, -23, -30, -16, -16, -23, -36, -32, 
                  -16, -27, 15, 6, 9, 17, 10, 5, 
                  -18, 28, 19, 47, 31, 34, 39, 23, 
                  3, 22, 24, 45, 57, 40, 57, 36, 
                  -20, 6, 9, 49, 47, 35, 19, 9, 
                  -17, 20, 32, 41, 58, 25, 30, 0, 
                  -9, 22, 22, 27, 27, 19, 10, 20],
    
    chess.KING: [-53, -34, -21, -11, -28, -14, -24, -43, 
                 -27, -11, 4, 13, 14, 4, -5, -17, 
                 -19, -3, 11, 21, 23, 16, 7, -9, 
                 -18, -4, 21, 24, 27, 23, 9, -11, 
                 -8, 22, 24, 27, 26, 33, 26, 3, 
                 10, 17, 23, 15, 20, 45, 44, 13, 
                 -12, 17, 14, 17, 17, 38, 23, 11, 
                 -74, -35, -18, -18, -11, 15, 4, -17]
}
base_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000 # must be this number
}
pieces_values = {chess.WHITE: base_values, chess.BLACK: base_values}

def evaluate(board: chess.Board) -> int:

    # Calculating phase
    pawn_phase = 0 # pawns arent important for calculating phase
    knight_phase = 1
    bishop_phase = 1
    rook_phase = 2
    queen_phase = 4

    total_phase = 24 # maximum possible phase, equals to pawn_phase*16 + knight_phase*4 + bishop_phase*4 + rook_phase*4 + queen_phase*2
    phase: int = total_phase

    white_pawns: chess.Bitboard = board.pieces_mask(chess.PAWN, chess.WHITE).bit_count()
    white_knights = board.pieces_mask(chess.KNIGHT, chess.WHITE).bit_count()
    white_bishops = board.pieces_mask(chess.BISHOP, chess.WHITE).bit_count()
    white_rooks = board.pieces_mask(chess.ROOK, chess.WHITE).bit_count()
    white_queens = board.pieces_mask(chess.QUEEN, chess.WHITE).bit_count()

    black_pawns = board.pieces_mask(chess.PAWN, chess.BLACK).bit_count()
    black_knights = board.pieces_mask(chess.KNIGHT, chess.BLACK).bit_count()
    black_bishops = board.pieces_mask(chess.BISHOP, chess.BLACK).bit_count()
    black_rooks = board.pieces_mask(chess.ROOK, chess.BLACK).bit_count()
    black_queens = board.pieces_mask(chess.QUEEN, chess.BLACK).bit_count()

    phase -= white_pawns * pawn_phase
    phase -= white_knights * knight_phase
    phase -= white_bishops * bishop_phase
    phase -= white_rooks * rook_phase
    phase -= white_queens * queen_phase

    phase -= black_pawns * pawn_phase
    phase -= black_knights * knight_phase
    phase -= black_bishops * bishop_phase
    phase -= black_rooks * rook_phase
    phase -= black_queens * queen_phase

    phase = (phase * 256 + (total_phase // 2)) // 256

    # Calculating midgame and endgame evaluation in White's perspective
    midgame_score = 0
    endgame_score = 0
    for piece_type in chess.PIECE_TYPES:
        for square in board.pieces(piece_type, chess.WHITE):
            midgame_score += MIDGAME_PST[piece_type][square]
            endgame_score += ENDGAME_PST[piece_type][square]

        for square in board.pieces(piece_type, chess.BLACK):
            flipped = chess.square_mirror(square)
            midgame_score -= MIDGAME_PST[piece_type][flipped]
            endgame_score -= ENDGAME_PST[piece_type][flipped]
    
    pawn_structure_score = pawn_structure(board)
    total = ((midgame_score * (256 - phase)) + (endgame_score * phase)) // 256
    total += pawn_structure_score
    return total