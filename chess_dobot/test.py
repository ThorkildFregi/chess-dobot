from serial.tools import list_ports
from time import sleep
import pydobot

# 50 -> 4.5
# 25 -> 2.25

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = pydobot.Dobot(port=port, verbose=True)

(x, y, z, r, j1, j2, j3, j4) = device.pose()
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device.move_to(123, 4, -17, 0, True)

device.move_to(x, 29, z, r, True)

sleep(2)

device.move_to(x, y, z, r, True)

device.close()