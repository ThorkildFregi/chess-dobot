from serial.tools import list_ports
import pydobot

# 50   -> 4.5
# 25   -> 2.25
# 12.5 -> 1.125

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = pydobot.Dobot(port=port, verbose=False)

base_coordinates = {"x": 143, "y": 4, "z": 25, "r": 0}
trash_coordinates = {"x": 151, "y": 234, "z": -4, "r": 0}

def to_base_coord():
    ### Move dobot to base coordinates ###

    device.move_to(base_coordinates["x"], base_coordinates["y"], base_coordinates["z"], base_coordinates["r"], True)

to_base_coord()

column = {"a" : -83.5, "b" : -58.5, "c" : -33.5, "d" : -8.5, "e" : 16.5, "f" : 41.5, "g" : 66.5, "h" : 91.5}
row = {"1" : 298, "2" : 273, "3" : 248, "4" : 223, "5" : 198, "6" : 173, "7" : 148, "8" : 123}

def take_piece(piece : str):
    ### Take the piece from the square ###

    (x, y, z, r, j1, j2, j3, j4) = device.pose()

    if piece == "PAWN":
        z = -20

    device.move_to(x, y, z, r, True)

    device.suck(True)

    device.move_to(x, y, base_coordinates["z"], r, True)

def drop_piece(piece : str):
    ### Take the piece from the square ###

    (x, y, z, r, j1, j2, j3, j4) = device.pose()

    if piece == "PAWN":
        z = -20

    device.move_to(x, y, z, r, True)

    device.suck(False)

    device.move_to(x, y, base_coordinates["z"], r, True)

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