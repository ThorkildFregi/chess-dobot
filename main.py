from stockfish import Stockfish

stockfish = Stockfish(path='./stockfish/stockfish-windows-x86-64-avx2.exe')

stockfish.set_skill_level(20)
print(stockfish.get_parameters())

print(stockfish.get_board_visual())

best_move = stockfish.get_best_move()
print(best_move)

stockfish.set_position([best_move ,"e7e6"])

print(stockfish.get_board_visual())
print(stockfish.get_best_move())
