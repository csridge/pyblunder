import random
import chess

# type annotation just in case i forgot how many dimensions do these have
zobrist_table: list[list[list[int]]] = [[[random.getrandbits(64) for _ in range(64)] for _ in range(2)] for _ in range(6)]
zobrist_castling: list[int] = [random.getrandbits(64) for _ in range(16)]
zobrist_en_passant = [random.getrandbits(64) for _ in range(8)]
zobrist_black_to_move = random.getrandbits(64)

def compute_zobrist_hash(board: chess.Board) -> int:
    h = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_index = piece.piece_type - 1  # 0-indexed
            color = 0 if piece.color == chess.WHITE else 1
            h ^= zobrist_table[piece_index][color][square]

    # Castling rights
    castling_state = 0
    if board.has_kingside_castling_rights(chess.WHITE): 
        castling_state |= 1
    if board.has_queenside_castling_rights(chess.WHITE): 
        castling_state |= 2
    if board.has_kingside_castling_rights(chess.BLACK): 
        castling_state |= 4
    if board.has_queenside_castling_rights(chess.BLACK): 
        castling_state |= 8
    h ^= zobrist_castling[castling_state]

    # En passant file (if any)
    if board.ep_square is not None:
        file = chess.square_file(board.ep_square)
        h ^= zobrist_en_passant[file]

    # Side to move
    h ^= zobrist_black_to_move if board.turn == chess.BLACK else 0

    return h