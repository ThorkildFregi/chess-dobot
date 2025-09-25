from flask import Flask, request, Response
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

is_playing = "" # Basic bool to know if play again
fen = ""

@app.route("/parameters", methods=["get"])
def param():
    if request.method == "GET":
        if not is_playing:
            skill_level = request.args.get("skilllevel", type=int)
            parameters = chess_move.set_game_parameters(skill_level)

            logging.info(parameters)

            return Response(json.dumps(parameters), status=202, mimetype="application/json")
        else:
            return Response(status=409)
    else:
        return Response(status=405)

@app.route("/start")
def start():
    if is_playing:
        return Response(status=409)
    else:
        is_playing = True # Party on going

        return Response(status=202)

@app.route("/makeamove", methods=["get"])
def make_a_move():
    if request.method == "GET":
        if is_playing:
            fen = request.args.get("fen", type=str)

            logging.info(chess_move.board_visual(fen))

            # Bot turn
            # Get bot move and if capture
            best_move, capture = chess_move.get_bot_move(fen)
            logging.info(best_move)

            # Move pieces with dobot
            # Get departure and arrival of the piece
            departure = best_move[0:2]
            arrival = best_move[2:4]

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
            
            return Response(json.dumps({"bot_move": best_move}), status=202, mimetype="application/json")   
        else:
            return Response(status=409)
    else:
        return Response(status=405)

if __name__ == "__main__":
    app.run()
