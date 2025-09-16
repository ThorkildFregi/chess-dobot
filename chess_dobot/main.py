from Chessnut.game import InvalidMove
from Chessnut import Game
import dobot_move
import chess_move
import logging

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

play_again = True # Basic bool to know if play again

while play_again:
    # Set skill of stockfish and print his parameters
    skill_level = int(input("Skill level of stockfish : "))
    logging.info(chess_move.set_game_parameters(skill_level))

    # Init chessgame with Chessnut
    chessgame = Game()
    logging.info(chess_move.board_visual(chessgame))

    checkmate = False
    while checkmate == False:
        # Checkmate detection
        if chessgame.get_moves() == []:
            logging.info("Checkmate")
            
            checkmate = True
            break
        
        # Ask player his move (potentially temp)
        move = input("Player move : ").replace(" ", "")
        
        try:
            # Player turn
            # Apply player move
            chessgame.apply_move(move)
            logging.info(chess_move.board_visual(chessgame))

            # Bot turn
            # Get bot move and if capture
            best_move, capture = chess_move.get_bot_move(chessgame)
            logging.info(best_move)

            # Apply bot move
            chessgame.apply_move(best_move)
            logging.info(chess_move.board_visual(chessgame))

            # Move pieces with dobot
            # Get departure and arrival of the piece
            departure = best_move[0:2]
            arrival = best_move[2:4]

            piece_departure = chess_move.get_piece_on_square(chessgame, departure)

            if capture == "DIRECT_CAPTURE": # If move a capture
                piece_arrival = chess_move.get_piece_on_square(chessgame, arrival)
                capture_piece(arrival, piece_arrival)
                move_piece(departure, arrival, piece_departure)
            elif capture == "EN_PASSANT": # If move en passant
                square_to_capture = arrival[0] + str(int(arrival[1]) + 1)
                piece_en_passant = chess_move.get_piece_on_square(chessgame, square_to_capture)
                capture_piece(square_to_capture, piece_en_passant)
                move_piece(departure, arrival, piece_departure)
            else:
                move_piece(departure, arrival, piece_departure)
        except InvalidMove: # Intercept exception if move is not valid from player and bot
            logging.error("Move not valid")
        
        logging.info(chessgame)
    
    play_again_input = input("Play Again ? ")

    if play_again_input.lower() == "no":
        play_again = False

dobot_move.stop_dobot()