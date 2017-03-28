
import time
import socket
import sys
import serial
import gripper_controller
import binascii
from crc16 import *

com = "/dev/ttyUSB0"
baud = 115200

robot = gripper_controller.gripper(mode = True)

robot.move(255, 255, 255)

#robot.shutdown()
sys.exit()
