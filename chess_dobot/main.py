from flask import Flask, request, Response, redirect, url_for
from utils import fendiff
import dobot_move
import chess_move
import logging
import json

app = Flask(__name__)

# Config for logging
logging.basicConfig(
    filename="./../temp/chess.log",  # Log file path
    filemode="w",
    datefmt="%d-%m %H:%M",
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    level=logging.INFO,  # Set to info level globally
)

# Create handler to show log
console = logging.StreamHandler()
console.setLevel(logging.INFO)  # Set console to info level

logging.getLogger("").addHandler(console)

def capture_piece(piece_square: str, piece: str):
    ### Take the piece to capture and throw it ###

    dobot_move.move_to_square(piece_square)
    dobot_move.throw_piece(piece)

def move_piece(departure: str, arrival: str, piece: str):
    ### Move a piece form a square to another ###

    dobot_move.move_to_square(departure)
    dobot_move.take_piece(piece)
    dobot_move.move_to_square(arrival)
    dobot_move.drop_piece(piece)
    dobot_move.to_base_coord()

def movement_board(move: str, capture: str):
    # Move pieces with dobot
    # Get departure and arrival of the piece
    departure = move[0:2]
    arrival = move[2:4]

    piece_departure = chess_move.get_piece_on_square(fen, departure)

    if capture == "DIRECT_CAPTURE": # If move a capture
        piece_arrival = chess_move.get_piece_on_square(fen, arrival)
        capture_piece(arrival, piece_arrival)
        move_piece(departure, arrival, piece_departure)
    elif capture == "EN_PASSANT": # If move en passant
        square_to_capture = arrival[0] + str(int(arrival[1]) + 1)
        piece_en_passant = chess_move.get_piece_on_square(fen, square_to_capture)
        capture_piece(square_to_capture, piece_en_passant)
        move_piece(departure, arrival, piece_departure)
    else:
        move_piece(departure, arrival, piece_departure)

def roquer(type: str, color: str):
    if color == "white":
        move_king = "e1g1"
        move_tower = "h1f1"
    else:
        move_king = "e8g8"
        move_tower = "h8f8"
    
    if type == "grand":
        move_king[3] = "c"
        move_tower[3] = "d"
    
    movement_board(move_king, "")
    movement_board(move_tower, "")

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
code = 0

@app.route("/")
def rest_api():
    return "It is a REST API for chess dobot, please don't interact with it here ! (or I will ban ip you ;) )"

@app.route("/resetparty")
def reset_party():
    global code
    global fen
    
    code = 0
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    return redirect(url_for("rest_api"))

@app.route("/start", methods=["get"])
def start():
    global code

    if request.method == "GET":
        new_code = request.args.get("code", type=int)

        if code == new_code:
            return Response(status=409)
        else:
            code = new_code
        
            skill_level = request.args.get("skilllevel", type=int)
            parameters = chess_move.set_game_parameters(skill_level)

            logging.info(parameters)

            return Response(json.dumps(parameters), status=202, mimetype="application/json")
    else:
        return Response(status=405)

@app.route("/join", methods=["get"])
def join():
    if request.method == "GET":
        code = request.args.get("code")

        if playing == code and fen != "":
            return Response(json.dumps({"fen": fen}), status=202, mimetype="application/json")
    else:
        return Response(status=405)

@app.route("/makeamove", methods=["get"])
def make_a_move():
    global fen

    if request.method == "GET":
        player_code = request.args.get("code", type=int)

        if code == player_code:
            new_fen = request.args.get("fen", type=str)
            move = fendiff(fen, new_fen)

            if move == "e1g1":
                roquer("petit", "white")
            elif move == "e1c1":
                roquer("grand", "white")

            capture = chess_move.get_capture(fen, move)

            logging.info(chess_move.board_visual(new_fen))

            movement_board(move, capture)

            fen = new_fen

            # Bot turn
            # Get bot move and if capture
            best_move, capture_bot, new_fen = chess_move.get_bot_move(fen)
            logging.info(best_move)

            if move == "e8g8":
                roquer("petit", "black")
            elif move == "e8c8":
                roquer("grand", "black")

            movement_board(best_move, capture_bot)

            fen = new_fen
            
            return Response(best_move, status=202, mimetype="text/html")
        else:
            return Response(status=409)
    else:
        return Response(status=405)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)