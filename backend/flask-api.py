from flask import Flask
from flask import request
from flask import jsonify
import platform
from stockfish import Stockfish
from flask_cors import CORS

from User import User
from Database import Database
from os import getenv

app = Flask(__name__)
db: Database
stockfish: Stockfish
CORS(app)

stockfish_path = {
    "Linux":   "./stockfish/stockfish-ubuntu-x86-64-modern",
    "Darwin":  "stockfish",  # for Mac; assuming you have already run "brew install stockfish"
    "Windows": r".\engine\stockfish-windows-x86-64-avx2.exe"
}

piece_abbr = {  # used for creating piece move to send to front end
    "KING":   "K",
    "QUEEN":  "Q",
    "ROOK":   "R",
    "BISHOP": "B",
    "KNIGHT": "N",
    "PAWN":   "P"
}

num_to_letter = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h"
}

letter_to_num = {v: k for k, v in num_to_letter.items()}


# @app.route("/make-move", methods=["POST"])
# def make_move():
#     """Adds move to the move order
#
#     Returns:
#         string: Status message
#     """
#     move = request.get_data().decode().strip("\"")
#     try:
#         stockfish.make_moves_from_current_position([move])
#     except:
#         return "Move was illegal and was not made"
#     moves.append(move)
#     return "Move added successfully"


@app.route("/get-moves", methods=["GET"])
def get_moves():
    """Prints a list of the moves made so far

    Returns:
        list: moves list
    """
    try:
        username = request.get_json()["username"]
        user = User(db, username)
        user.load()  # fetch list of users games from db. Games not yet loaded.
        game = user.games[-1]  # most recent game
        game.load()
        game_moves = [move.move for move in game.moves]
        return game_moves
    except Exception as e:
        print(f"Error: {e}")


@app.route("/see-board", methods=["GET"])
def see_board():
    """Calls the stockfish engine to print out a visual of the current board state

    Returns:
        string: A formatted visual of the currrent board state
    """
    return stockfish.get_board_visual()


@app.route("/start-with-white", methods=["POST"])
def start_with_white():
    try:
        username = request.get_json()["username"]
        user = User(db, username)
        user.save()  # create or fetch user.
        game = user.new_game()
        game.save()  # create empty game in db.
    except Exception as e:
        print(f"Error: {e}")
    stockfish.set_position([])
    return "Ready to start"


@app.route("/start-with-black", methods=["GET"])
def start_with_black():
    username = request.get_json()["username"]
    try:
        user = User(db, username)
        user.save()  # create or fetch user.
        game = user.new_game()
        game.save()  # create emtpy game in db.
        engine_move = stockfish.get_best_move()
        game.add_move(engine_move)
        game_moves = [move.move for move in game.moves]
        stockfish.make_moves_from_current_position(game_moves)
        return engine_move
    except Exception as e:
        print(f"Error: {e}")


@app.route("/play", methods=["POST"])
def play():
    """Stores a move made by the player, then uses stockfish to find the best move and returns the result

    Returns:
        string: The resulting board state after stockfish makes its move
    """
    username = request.get_json()["username"]
    currX = request.get_json()["currX"]
    currY = request.get_json()["currY"]
    newX = request.get_json()["newX"]
    newY = request.get_json()["newY"]

    currX = num_to_letter[currX]
    currY += 1
    newX = num_to_letter[newX]
    newY += 1
    move = currX + str(currY) + newX + str(newY)

    # TODO: front end will send moves as coordinates; need to decode
    try:
        stockfish.make_moves_from_current_position([move])
    except:
        # return "Move was illegal and was not made"
        # response = jsonify({'error': 'Invalid move'})
        return "Move was illegal and was not made", 400
    try:
        user = User(db, username)
        user.load()
        game = user.games[-1]
        game.load()  # fetch moves of most recent game from db.

        game.add_move(move)
        engine_move = stockfish.get_best_move()
        game.add_move(engine_move)
        stockfish.make_moves_from_current_position([engine_move])

        engine_origin = engine_move[:2]
        engine_dest = engine_move[-2:]
        engine_piece = str(stockfish.get_what_is_on_square(engine_dest))
        piece_type = engine_piece[engine_piece.find("_") + 1:]
        print(piece_abbr[piece_type] + engine_dest)

        old_engine_x = letter_to_num[engine_origin[0]]
        old_engine_y = int(engine_origin[1]) - 1
        new_engine_x = letter_to_num[engine_dest[0]]
        new_engine_y = int(engine_dest[1]) - 1

        # return stockfish.get_board_visual()
        return jsonify(
            {
                "old_engine_x": old_engine_x,
                "old_engine_y": old_engine_y,
                "new_engine_x": new_engine_x,
                "new_engine_y": new_engine_y
            }
            )
        # TODO: This will need to change when integrated with front end;
        # just prints what the board looks like as of now.

    except Exception as e:
        print(f"Error: {e}")


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


# @app.route("/reset", methods=["POST"])
# def reset():
#     """Sets the board state and engine back to a start-of-game state. Will be most useful
#     for analysis, which will allow for easy switching between games.
#
#     Returns:
#         string: Status message
#     """
#     moves = []
#     stockfish.set_position([])
#     return "Game state reset"

@app.route("/five-best", methods=["GET"])
def get_5_best_moves():
    try:
        return stockfish.get_top_moves(5)
    except:
        return "Stockfish encountered an error"


@app.route("/get-eval", methods=["GET"])
def get_eval():
    try:
        return stockfish.get_evaluation()
    except:
        return "Stockfish encountered an error"


# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json()
#     username = data["username"]
#     pw = data["password"]
#
#     # TODO: Send this data to DB, get back user info if applicable
#     return "User logged in"


# @app.route("/create-user", methods=["POST"])
# def create_user():
#     data = request.get_json()
#     username = data["username"]
#     pw = data["password"]
#     print("Username:", username)
#     print("Password:", pw)
#
#     # TODO: Send data to DB, create the user if they don't exist already
#     return "User created"


# run using "python3 flask-test.py"
# DB_SCHEMA=backend;DB_PASS=real_good_password;DB_USER=root;DB_HOST=localhost;DB_PORT=3306
if __name__ == "__main__":
    stockfish = Stockfish(
        path=stockfish_path[platform.system()],
        # path="stockfish"
        depth=18,
        parameters={
            "Threads":           4,
            # Adapt this to the VM that runs the engine; optimal is to use all available threads
            "Ponder":            "true",  # Set to false to make the engine weaker
            "MultiPV":           1,
            # This may need to be changed for analysis if multiple variations need to outputted
            #   "Skill level": 20,    # Default skill level; could be overriden if it does not match ELO
            #   "Move overhead": 100, # Adds 100ms delay to account for network/GUI latency
            "Slow Mover":        50,
            "UCI_Chess960":      "false",
            "UCI_LimitStrength": "true",  # Enables skill level override
            "UCI_Elo":           1000
        }
    )
    db = Database(
        {
            'user':              getenv("DB_USER"),
            'password':          getenv("DB_PASS"),
            'database':          getenv("DB_SCHEMA"),
            'host':              getenv("DB_HOST"),
            'port':              getenv("DB_PORT"),
            'raise_on_warnings': True,
        }
    )
    app.run(host='0.0.0.0', port=105)
    # app.run(host='0.0.0.0', port=105, ssl_context='adhoc')
