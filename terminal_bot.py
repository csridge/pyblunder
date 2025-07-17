import chess
import chess.polyglot
import time
from negamax import negamax
from evaluate import evaluate
import sys
MAX_DEPTH = 4
def get_move(board: chess.Board):
    try:
        if board.fullmove_number <= 12:
            with chess.polyglot.open_reader("komodo.bin") as reader:
                move = reader.weighted_choice(board).move
                evaluation = evaluate(board)
                return evaluation, move
    except IndexError:
        pass
    except FileNotFoundError:
        print("Opening book file not found.")
    
    return negamax(board, MAX_DEPTH, float('-inf'), float('inf'), is_root=True)

def parse_input_move(board: chess.Board, move_str: str) -> chess.Move | None:
    try:
        return board.parse_san(move_str)
    except ValueError:
        try:
            return chess.Move.from_uci(move_str)
        except ValueError:
            return None

def main():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            user_input = input("Enter your move (e.g., e4 or e2e4): ")
            if user_input.lower() == "quit":
                sys.exit()
            move = parse_input_move(board, user_input)
            if not move:
                print("Illgal move. Please try again.")
                continue

            if move in board.legal_moves:
                board.push(move)
            else:
                print("Invalid move.")
                continue
        else:
            print("Bot is thinking...")
            start = time.time()
            eval, move = get_move(board)
            elapsed = time.time() - start
            if not move:
                print("There are no legal moves left.")
                continue
            print(f"Bot plays: {board.san(move)}  (Eval: {(eval/100):.2f}, Time: {elapsed:.2f}s)")
            board.push(move)
        print(board)

    print("Game over!")
    print(board.result())

if __name__ == "__main__":
    main()
