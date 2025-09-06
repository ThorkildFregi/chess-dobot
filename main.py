from Chessnut.game import InvalidMove
from Chessnut import Game
from chess_move import *

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