import time
from stockfish import Stockfish # need to use Homebrew to install, doesn't just work with pip

stockfish = Stockfish(path="/usr/local/Cellar/stockfish/16/bin/stockfish", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})

print(stockfish.get_parameters())

# allows to be set based on move order. Seems like the best option
stockfish.set_position(["e2e4", "e7e6", "g1f3"])
print(stockfish.get_board_visual())

# will return True, however this formate may not be the best to use since it is difficult to generate
start_time = time.time()
print(stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")) # will return False, in this case because the FEN is missing two of the six required fields.
print("--- %s seconds ---" % (time.time() - start_time))

# seems like best move often takes ~0.5 seconds running locally with current configuration; may vary with different parameters and on Docker container
start_time = time.time()
print(stockfish.get_best_move())
print("--- %s seconds ---" % (time.time() - start_time))