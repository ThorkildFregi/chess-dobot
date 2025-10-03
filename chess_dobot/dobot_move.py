from serial.tools import list_ports
from time import sleep
import pydobot

# 50   -> 4.5
# 25   -> 2.25
# 12.5 -> 1.125

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = pydobot.Dobot(port=port, verbose=False)
device.suck(False)

base_coordinates = {"x": 143, "y": 4, "z": 20, "r": 0}
trash_coordinates = {"x": 151, "y": 234, "z": -4, "r": 0}

def to_base_coord():
    ### Move dobot to base coordinates ###

    device.move_to(base_coordinates["x"], base_coordinates["y"], base_coordinates["z"], base_coordinates["r"], True)

to_base_coord()

column = {"a" : -76, "b" : -55, "c" : -32, "d" : -11, "e" : 14, "f" : 35, "g" : 59, "h" : 80}
row = {"1" : 293, "2" : 273, "3" : 249, "4" : 228, "5" : 203, "6" : 183, "7" : 159, "8" : 137}
height = {"PAWN" : -21, "ROOK" : -17, "KING" : -12, "QUEEN" : -12 , "KNIGHT" : -12, "BISHOP" : -11}

def take_piece(piece : str):
    ### Take the piece from the square ###

    (x, y, z, r, j1, j2, j3, j4) = device.pose()

    device.move_to(x, y, height[piece], r, True)

    device.suck(True)

    sleep(1)

    device.move_to(x, y, z, r, True)

def drop_piece(piece : str):
    ### Take the piece from the square ###

    (x, y, z, r, j1, j2, j3, j4) = device.pose()

    device.move_to(x, y, height[piece], r, True)

    device.suck(False)

    sleep(1)

    device.move_to(x, y, z, r, True)

def move_to_square(square : str):
    ### Move dobot to a specific square ###

    column_coord = column[square[0]]
    row_coord = row[square[1]]

    device.move_to(row_coord, column_coord, base_coordinates["z"], base_coordinates["r"], True)

def throw_piece(piece : str):
    ### Throw enemy piece in a trash ###

    take_piece(piece)

    device.move_to(trash_coordinates["x"], trash_coordinates["y"], trash_coordinates["z"], trash_coordinates["r"], True)

    device.suck(False)

def stop_dobot():
    ### Stop dobot ###

    device.close()