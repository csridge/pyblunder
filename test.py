import chess
import time
def flip_pst_ranks(pst: list[int]) -> list[int]:
    return sum([pst[i*8:(i+1)*8] for i in reversed(range(8))], [])
print(flip_pst_ranks([
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]))

pawn_phase = 0 # pawns arent important for calculating phase
knight_phase = 1
bishop_phase = 1
rook_phase = 2
queen_phase = 4

print(pawn_phase*16 + knight_phase*4 + bishop_phase*4 + rook_phase*4 + queen_phase*2)