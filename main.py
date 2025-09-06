from chess_move import *

play = True

while play:
    skill_level = int(input("Skill level of stockfish"))

    set_game_parameters(skill_level)

    new_game()
    
    