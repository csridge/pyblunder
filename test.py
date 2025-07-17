import chess
import time
start = time.time()
board = chess.Board()
print(bin(board.occupied_co[chess.WHITE]).count('1'))
end = time.time()
print(end-start, "s")