import chess
import time
from bot import negamax  # your negamax search

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
            move = parse_input_move(board, user_input)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Invalid move.")
                continue
        else:
            print("Bot is thinking...")
            start = time.time()
            eval, move = negamax(board, 4, float('-inf'), float('inf'))
            elapsed = time.time() - start
            print(f"Bot plays: {board.san(move)}  (Eval: {eval:.2f}, Time: {elapsed:.2f}s)")
            board.push(move)
        print(board)
        print()

    print("Game over!")
    print(board.result())

if __name__ == "__main__":
    main()
