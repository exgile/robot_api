"""#!/usr/bin/env python"""
from config import *
from crc16 import * 
from time import sleep
import serial
import binascii
import sys


def _packet(packet) :
	return binascii.unhexlify(packet)

class gripper :
	def __init__(self, COM = "/dev/ttyUSB0", baudrate = 115200, timeout = 1, mode = False) :
		self.COM = COM
		self.baud = baudrate
		self.timeout = timeout
		self.mode = mode            # Secure mode
		self.s = serial.Serial(self.COM, self.baud, timeout = self.timeout)

		self.gripperReset()

	def move_gen(self, pose, force, speed) :
		data = BASIC_MOVE_COMMAND + format(pose, '02x') + format(force, '02x') + format(speed, '02x')
		return GetCrc16(data)

	def gripperReset(self) :
		self.s.write(_packet(RESET_INIT_ACT))
		sleep(0.1)
		self.s.write(_packet(SET_INIT_ACT))

		while True :
			self.s.write(_packet(WAIT_INIT_ACT))
			data_raw = self.s.readline()

			if binascii.hexlify(data_raw) == INIT_ACT_COMPLETE :
				#print("Complete move")
				break

	def close(self) :
		self.move(pose = 255)

	def open(self) :
		self.move(pose = 0)

	def move(self, pose, force = 255, speed = 255) :
		# Default speed, force = 255 , (range 0~255)
		if self.mode is True :
			force = 0
			speed = 0

		command = self.move_gen(pose, force, speed)

		self.s.write(_packet(command)) # Move Position

		while True : 
			self.s.write(_packet(WAIT_MOVE))
			data_raw = self.s.readline() # data read

			data = binascii.hexlify(data_raw) # \x09\x03 -> 0903  : to ascii

			# Data = 09 03 06 xx 00 yy uu zz zz
			# xx 00 : xx = Gripper status 
			# yy uu : yy = Fault status(00), uu = Position request echo,(desired pose)
			# zz zz : crc packet

			status = [data[6:8], data[10:12], data[12:14]]
			
			if status[0] == 'b9' :
				print("Object detection")
				break

			elif status[0] == 'f9' :
				print("Correct pose")
				break

	def shutdown(self) :
		self.s.close()