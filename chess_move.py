from stockfish import Stockfish
from typing import Dict

stockfish = Stockfish(path='./stockfish/stockfish-windows-x86-64-avx2.exe')

def board_visual():
    print(stockfish.get_board_visual())

def set_game_parameters(skill_level: int = 20) -> Dict:
    stockfish.reset_engine_parameters()

    stockfish.set_skill_level(20)

    return stockfish.get_parameters()

def new_game():
    stockfish.set_position([])

    print("Starting game...")

def player_move(move: str) -> str:
    if stockfish.is_move_correct(move):
        stockfish.make_moves_from_current_position([move])
    
    return stockfish.get_board_visual()

def bot_move() -> str:
    best_move = stockfish.get_best_move()

    stockfish.make_moves_from_current_position([best_move])

    return stockfish.get_board_visual()