from stockfish import Stockfish
from typing import Dict

# Init stockfish from intern download
stockfish = Stockfish()

def board_visual(fen: str) -> str:
    ### Return a string with board visual in ASCII ###

    stockfish.set_fen_position(fen) # Init the game in stockfish with the actual fen

    return stockfish.get_board_visual()

def set_game_parameters(skill_level: int = 20) -> Dict:
    ### Change stockfish skill level and return stockfish parameters ###

    stockfish.reset_engine_parameters()

    stockfish.set_skill_level(skill_level) # Change skill of stockfish

    return stockfish.get_parameters()

def get_bot_move(fen: str) -> (str, str):
    ### Return best move found by Stockfish and if it is a capture ###

    stockfish.set_fen_position(fen)

    best_move = stockfish.get_best_move() # Get best moves to play with actual fen
    capture = str(stockfish.will_move_be_a_capture(best_move)).replace("Capture.", "")

    stockfish.make_moves_from_current_position([best_move])

    return best_move, capture, stockfish.get_fen_position()

def get_piece_on_square(fen: str, square: str):
    ### Get the piece on a square ###

    stockfish.set_fen_position(fen)

    return str(stockfish.get_what_is_on_square(square)).replace("Capture.", "")

def get_capture(fen: str, move: str):
    #### Get if move a capture and what ###

    stockfish.set_fen_position(fen)

    return str(stockfish.will_move_be_a_capture(move)).replace("Capture.", "")