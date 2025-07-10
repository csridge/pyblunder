import chess
from evaluate import evaluate
from zobrist import compute_zobrist_hash
from typing import Tuple
from typing import Optional
import sys
board = chess.Board() # da board!!!

# piece values
pieces_val = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 69420 # must be this number
}
center = [chess.C3, chess.C4, chess.C5, chess.C6,
          chess.D3, chess.D4, chess.D5, chess.D6, 
          chess.E3, chess.E4, chess.E5, chess.E6,
          chess.F3, chess.F4, chess.F5, chess.F6] # center squares

# minimax algorithm + alpha beta pruning
def is_attacking_center(board):
    for square in center:
        attackers = board.attackers(chess.BLACK, square)
        if attackers:
            return True
    return False

history_table = [[0 for _ in range(64)] for _ in range(64)]
def move_score(board: chess.Board, move: chess.Move) -> int:
    score = 0

    if board.is_capture(move) or board.is_en_passant(move):
        captured_piece = board.piece_at(move.to_square)
        capturing_piece = board.piece_at(move.from_square)

        if captured_piece and capturing_piece:  # prevent NoneType errors
            score += 10 * pieces_val[captured_piece.piece_type]
            score -= pieces_val[capturing_piece.piece_type]

    if board.gives_check(move):
        score += 40

    if board.is_castling(move):
        score += 100

    if move.promotion:
        score += pieces_val[move.promotion]

    from_sq, to_sq = move.from_square, move.to_square
    score += history_table[from_sq][to_sq]

    return score

def sort_moves(board: chess.Board):
    return sorted(board.legal_moves, key=lambda move: move_score(board, move), reverse=True)
def quiescenceSearch(board: chess.Board, alpha: float, beta: float):
    stand_pat: float = evaluate(board)

    noisy_moves = [move for move in board.legal_moves if board.is_capture(move)]
    best_eval: float = stand_pat
    if best_eval >= beta:
        return best_eval
    if best_eval > alpha:
        alpha = best_eval
    for move in noisy_moves:
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

def negamax(board: chess.Board, depth: int, alpha: float, beta: float) -> Tuple[float, Optional[chess.Move]]:
    key = compute_zobrist_hash(board)

    if key in transposition_table:
        entry = transposition_table[key]
        if entry["depth"] >= depth:
            return entry["evaluation"], entry.get("move")
        
    CHECKMATE_SCORE = 20000.0
    if board.is_checkmate():
        return -CHECKMATE_SCORE + depth, None
    if depth == 0 or board.is_game_over():
        global position_evaluated
        position_evaluated += 1
        score = -evaluate(board)
        transposition_table[key] = {
            "depth": depth,
            "evaluation": score,
            "move": None  # no best move at leaf
        }
        return score, None
    
    max_eval = float('-inf')
    best_move = None

    moves = list(board.legal_moves)
    for i, move in enumerate(moves):
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

        if evaluation > max_eval and move in board.legal_moves:
            max_eval = evaluation
            best_move = move

        alpha = max(alpha, evaluation)
        if alpha >= beta:
            from_sq, to_sq = move.from_square, move.to_square
            history_table[from_sq][to_sq] += depth * depth
            break  # Beta cutoff
    
    transposition_table[key] = {
        "depth": depth,
        "evaluation": max_eval,
        "move": best_move
    }
    return max_eval, best_move

def parse_input_move(board: chess.Board, move_str: str) -> Optional[chess.Move]:
    try:
        return board.parse_san(move_str)  # try SAN (e.g. "Nf3")
    except ValueError:
        try:
            return chess.Move.from_uci(move_str)  # try UCI (e.g. "g1f3")
        except ValueError:
            return None  # Invalid input

print(f"{board}\n\n")

def main():
    board = chess.Board()

    while True:
        line = sys.stdin.readline().strip()
        if line == "":
            continue

        if line == "uci":
            print("id name jsaidorubot", flush=True)
            print("id author jsaidoru", flush=True)
            print("uciok", flush=True)

        elif line == "isready":
            print("readyok", flush=True)

        elif line.startswith("ucinewgame"):
            board.reset()

        elif line.startswith("position"):
            # Handle Arena setting up a position
            parts = line.split()
            if "startpos" in parts:
                board.set_fen(chess.STARTING_FEN)
                if "moves" in parts:
                    moves_index = parts.index("moves")
                    for move in parts[moves_index + 1:]:
                        board.push_uci(move)
            elif "fen" in parts:
                fen_index = parts.index("fen")
                fen_parts = parts[fen_index + 1:]
                if "moves" in parts:
                    moves_index = parts.index("moves")
                    fen = " ".join(parts[fen_index + 1: moves_index])
                    board.set_fen(fen)
                    for move in parts[moves_index + 1:]:
                        board.push_uci(move)
                else:
                    fen = " ".join(fen_parts)
                    board.set_fen(fen)

        elif line.startswith("go"):
            # Perform search and return best move
            _, best_move = negamax(board, 4, float('-inf'), float('inf'))
            if best_move is not None:
                print(f"bestmove {best_move.uci()}", flush=True)
            else:
                print("bestmove 0000", flush=True)  # No legal moves

        elif line == "quit":
            break

if __name__ == "__main__":
    main()