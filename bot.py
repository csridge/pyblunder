import sys
import traceback
try:
    import chess
    import chess.polyglot
    from negamax import negamax
    from typing import Optional
    from evaluate import evaluate
    import sys
    board = chess.Board() # da board!!!

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

        return negamax(board, depth=MAX_DEPTH, alpha=float('-inf'), beta=float('inf'), is_root=True, max_depth=MAX_DEPTH)
    def parse_input_move(board: chess.Board, move_str: str) -> Optional[chess.Move]:
        try:
            return board.parse_san(move_str)
        except ValueError:
            try:
                return chess.Move.from_uci(move_str)
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
                print("id name pyblunder", flush=True)
                print("id author jsaidoru", flush=True)
                print("option name Move Overhead type spin default 30 min 0 max 5000", flush=True)
                print("option name Threads type spin default 1 min 1 max 128", flush=True)
                print("option name Hash type spin default 16 min 1 max 1024", flush=True)
                print("option name SyzygyPath type string default <empty>", flush=True)
                print("option name UCI_ShowWDL type check default false", flush=True)
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
                _, best_move = get_move(board)
                if best_move is not None:
                    print(f"bestmove {best_move.uci()}", flush=True)
                else:
                    print("bestmove 0000", flush=True)  # No legal moves

            elif line == "quit":
                break

    if __name__ == "__main__":
        main()
except Exception as e:
    traceback.print_exc()
    sys.exit(1)