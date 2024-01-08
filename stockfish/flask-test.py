from flask import Flask
from flask import request
from flask import jsonify
import json

from stockfish import Stockfish

app = Flask(__name__)
stockfish = Stockfish(path="/usr/local/Cellar/stockfish/16/bin/stockfish", 
                      depth=18, 
                      parameters={"Threads": 4,         # Adapt this to the VM that runs the engine; optimal is to use all available threads
                                  "Ponder": "true",     # Set to false to make the engine weaker
                                  "MultiPV": 1,         # This may need to be changed for analysis if multiple variations need to outputted
                                  "Skill level": 20,    # Default skill level; could be overriden if it does not match ELO
                                  "Move overhead": 100, # Adds 100ms delay to account for network/GUI latency
                                  "Slow Mover": 50, 
                                  "UCI_Chess960": "false", 
                                  "UCI_LimitStrength": "true",  # Enables skill level override
                                  "UCI_Elo": 1000
                                  })

moves = []      # current way to store game state; should be sent to database eventually somehow

@app.route("/make-move", methods=["POST"])
def make_move():
    """Adds move to the move order

    Returns:
        string: Status message
    """
    move = request.get_data().decode().strip("\"")
    try:
        stockfish.make_moves_from_current_position([move])
    except:
        return "Move was illegal and was not made"
    moves.append(move)
    return "Move added successfully"

@app.route("/get-moves", methods=["GET"])
def get_moves():
    """Prints a list of the moves made so far

    Returns:
        list: moves list
    """
    return moves

@app.route("/see-board", methods=["GET"])
def see_board():
    """Calls the stockfish engine to print out a visual of the current board state

    Returns:
        string: A formatted visual of the currrent board state
    """
    return stockfish.get_board_visual()

# stores a move given by the player, then finds the best move and prints the resulting board back to the player
@app.route("/play", methods=["POST"])
def play():
    """Stores a move made by the player, then uses stockfish to find the best move and returns the result

    Returns:
        string: The resulting board state after stockfish makes its move
    """
    move = request.get_data().decode().strip("\"")
    try:
        stockfish.make_moves_from_current_position([move])
    except:
        return "Move was illegal and was not made"
    
    moves.append(move)
    engine_move = stockfish.get_best_move()
    moves.append(engine_move)
    stockfish.make_moves_from_current_position([engine_move])
    return stockfish.get_board_visual()     # TODO: This will need to change when integrated with front end; 
                                            # just prints what the board looks like as of now.
                                            # Should return engine_move, assuming front end can process that

@app.route("/change-elo", methods=["POST"])
def change_elo():
    """Changes the ELO of the engine, which will also affect strength

    Returns:
        string: Status message
    """
    new_elo = request.get_data().decode().strip("\"")
    print(int(new_elo))
    try:
        stockfish.set_elo_rating(new_elo)
    except:
        return "ELO could not be changed"
    
    return f"Changed ELO to {new_elo}"

@app.route("/reset", methods=["POST"])
def reset():
    """Sets the board state and engine back to a start-of-game state. Will be most useful 
    for analysis, which will allow for easy switching between games.

    Returns:
        string: Status message
    """
    moves = []
    stockfish.set_position([])
    return "Game state reset"

# run using "python3 flask-test.py"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=105)