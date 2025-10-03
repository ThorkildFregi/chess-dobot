from flask import Flask, request, Response, render_template
from time import perf_counter
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

base_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
party_debut = 0.
fen = base_fen
params = []
code = 0

def no_party_on_going():
    global code
    global fen

    code = 0
    fen = ""

def new_party(new_code: int, skill_level: int):
    global code
    global fen

    code = new_code
    fen = base_fen

    parameters = chess_move.set_game_parameters(skill_level)
    logging.info(parameters)

    return parameters

@app.route("/")
def rest_api():
    return "It is a REST API for chess dobot, please don't interact with it here ! (or I will ban ip you ;) )"

@app.route("/installation")
def installation():
    return render_template("installation.html")

@app.route("/resetparty")
def reset_party():
    global params

    if params != []:
        new_party(params[0]["code"], params[0]["skill_level"])

        del params[0]
    else:
        no_party_on_going()

    return Response(status=202)

@app.route("/erasefromwaitingqueue", methods=["get"])
def erase_from_waiting_queue():
    global params

    if request.method == "GET":
        index = request.args.get("index", type=int)

        del params[index]

        return Response(status=202)
    else:
        return Response(status=405)

@app.route("/start", methods=["get"])
def start():
    global params

    if request.method == "GET":
        name = request.args.get("name", type=str)
        new_code = request.args.get("code", type=int)
        skill_level = request.args.get("skilllevel", type=int)

        if any([new_code == param["code"] for param in params]) or new_code == code:
            return Response(status=409)
        else:
            if code == 0:
                param = new_party(new_code, skill_level)

                return Response(json.dumps(param), status=202, mimetype="application/json")
            else:
                params.append({"name" : name, "code" : new_code, "skill_level" : skill_level})

                return Response(str(len(params)), status=201, mimetype="text/plain")
    else:
        return Response(status=405)

@app.route("/join", methods=["get"])
def join():
    if request.method == "GET":
        global code

        player_code = request.args.get("code", type=int)

        if code != 0:
            if player_code == code:
                return Response(fen, status=202, mimetype="text/html")
            else:
                return Response(status=403)
        else:
            return Response(status=400)
    else:
        return Response(status=405)

@app.route("/makeamove", methods=["get"])
def make_a_move():
    global party_debut
    global params
    global fen

    if request.method == "GET":
        player_code = request.args.get("code", type=int)

        if code == player_code:
            party_time = party_debut - perf_counter()

            if fen == base_fen:
                party_debut = perf_counter()
            elif party_time >= 300:
                if params != []:
                    new_party(params[0]["code"], params[0]["skill_level"])

                    del params[0]

                    return Response(status=408)
                else:
                    no_party_on_going()

                    return Response(status=408)

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