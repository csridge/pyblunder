import chess
from zobrist import compute_zobrist_hash
from typing import Optional
from evaluate import evaluate
pieces_val = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 69420 # must be this number
}

MAX_DEPTH = 4
# minimax algorithm + some opmizations

history_table = [[0 for _ in range(64)] for _ in range(64)] # Initialize table with a 2x2 array
def move_score(board: chess.Board, move: chess.Move) -> int:
    score = 0

    if board.is_capture(move) or board.is_en_passant(move):
        captured_piece = board.piece_at(move.to_square)
        capturing_piece = board.piece_at(move.from_square)

        if captured_piece and capturing_piece:  # prevent NoneType errors
            score += 10 * pieces_val[captured_piece.piece_type]
            score -= pieces_val[capturing_piece.piece_type]

    if board.gives_check(move):
        score += 30

    if board.is_castling(move):
        score += 100

    if move.promotion:
        score += pieces_val[move.promotion]

    from_sq, to_sq = move.from_square, move.to_square
    score += history_table[from_sq][to_sq]
    

    return score

def sort_moves(board: chess.Board):
    return sorted(board.legal_moves, key=lambda move: move_score(board, move), reverse=True)
    # Reverse for best moves first
def quiescenceSearch(board: chess.Board, alpha: float, beta: float):
    DELTA_MARGIN = 200
    stand_pat: float = evaluate(board)

    noisy_moves = [move for move in board.legal_moves if board.is_capture(move) or board.is_en_passant(move)]
    best_eval: float = stand_pat
    if best_eval >= beta:
        return best_eval
    if best_eval > alpha:
        alpha = best_eval

    for move in noisy_moves:
        capturing_piece = board.piece_at(move.from_square)

        if board.is_en_passant(move):
            captured_piece = chess.Piece(chess.PAWN, not board.turn)
        else:
            captured_piece = board.piece_at(move.to_square)

        if captured_piece is not None and capturing_piece is not None:
            gain = pieces_val[captured_piece.piece_type] - pieces_val[capturing_piece.piece_type]
        else:
            gain = 0
        if stand_pat + gain + DELTA_MARGIN < alpha:
            return alpha # this capture doesnt improve the material much, therefore pruning
        board.push(move)
        evaluation = -quiescenceSearch(board, -beta, -alpha)
        board.pop()

        if evaluation >= beta:
            return evaluation
        if evaluation > best_eval:
            best_eval = evaluation
        if evaluation > alpha:
            alpha = evaluation
    return best_eval

position_evaluated: int = 0
transposition_table: dict = {}
def negamax(board: chess.Board, depth: int, alpha: float, beta: float) -> tuple[float, Optional[chess.Move]]:
    key = compute_zobrist_hash(board)

    if key in transposition_table:
        entry = transposition_table[key]
        if entry["depth"] >= depth:
            return entry["evaluation"], entry.get("move")
        
    CHECKMATE_SCORE = 20000.0
    if board.is_checkmate():
        return -CHECKMATE_SCORE + depth, None
    if depth == 0 or board.is_game_over():
        score = -quiescenceSearch(board, alpha, beta)
        transposition_table[key] = {
            "depth": depth,
            "evaluation": score,
            "move": None  # no best move at leaf
        }
        return score, None
    
    max_eval = float('-inf')
    best_move = None

    for i, move in enumerate(sort_moves(board)):
        board.push(move)

        if i == 0:
            eval_score, _ = negamax(board, depth - 1, -beta, -alpha)
            evaluation = -eval_score
        else:
            # Null window search
            eval_score, _ = negamax(board, depth - 1, -alpha - 1, -alpha)
            evaluation = -eval_score

            # Fail-high: re-search with full window
            if alpha < evaluation < beta:
                eval_score, _ = negamax(board, depth - 1, -beta, -evaluation)
                evaluation = -eval_score

        board.pop()

        if evaluation > max_eval:
            max_eval = evaluation
            best_move = move

        alpha = max(alpha, evaluation)
        if alpha >= beta:
            from_sq, to_sq = move.from_square, move.to_square
            history_table[from_sq][to_sq] += depth * depth
            break
    
    if depth >= 3:
        transposition_table[key] = {
            "depth": depth,
            "evaluation": max_eval,
            "move": best_move
        }
    return max_eval, best_move