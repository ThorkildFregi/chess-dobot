from Chessnut.game import InvalidMove
from serial.tools import list_ports
from Chessnut import Game
from chess_move import *
import pydobot

# 50 -> 4.5
# 25 -> 2.25

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = pydobot.Dobot(port=port, verbose=True)

base_coordinates = {"x": 123, "y": 4, "z": -17, "r": 0}

device.move_to(123, 4, -17, 0, True)

column = {"e" : 29}
row = {}

play = True

while play:
    skill_level = int(input("Skill level of stockfish : "))

    print(set_game_parameters(skill_level))

    chessgame = Game()
    print(board_visual(chessgame))

    checkmate = False
    while checkmate == False:
        if chessgame.get_moves() == []:
            print("Checkmate")
            
            checkmate = True
            break

        move = input("Player move : ")
        
        try:
            chessgame.apply_move(move)
            print(board_visual(chessgame))

            best_move = get_bot_move(chessgame)
            print(best_move)

            chessgame.apply_move(best_move)
            print(board_visual(chessgame))
        except InvalidMove:
            print("Move not valid") 
    
    play_again = input("Play Again ? ")

    if play_again.lower() == "no":
        play = False

device.close()