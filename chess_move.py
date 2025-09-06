from stockfish import Stockfish
from typing import Dict

stockfish = Stockfish(path='./stockfish/stockfish-windows-x86-64-avx2.exe')

def board_visual(fen: str) -> str:
    stockfish.set_fen_position(fen)

    return stockfish.get_board_visual()

def set_game_parameters(skill_level: int = 20) -> Dict:
    stockfish.reset_engine_parameters()

    stockfish.set_skill_level(20)

    return stockfish.get_parameters()

def get_bot_move(fen: str) -> str:
    stockfish.set_fen_position(fen)

    best_move = stockfish.get_best_move()

    return best_move