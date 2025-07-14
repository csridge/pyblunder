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
            with chess.polyglot.open_reader("baron30.bin") as reader:
                move = reader.weighted_choice(board).move
                evaluation = evaluate(board)
                return evaluation, move
    except IndexError:
        print("No book moves found.")
    except FileNotFoundError:
        print("Opening book file not found.")
    
    return negamax(board, MAX_DEPTH, float('-inf'), float('inf'))

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
            print(f"Bot plays: {board.san(move)}  (Eval: {(eval/100):.2f}, Time: {elapsed:.2f}s)")
            board.push(move)
        print(board)

    print("Game over!")
    print(board.result())

if __name__ == "__main__":
    main()
