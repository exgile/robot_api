import time
import socket
import sys

HOST = '192.168.0.11'
PORT = 30002
PORT2 = 502
BUFSIZE = 1024
ADDR = (HOST, PORT)

ADDR2 = (HOST, PORT2)

a_joint = 1.2
v_joint = 0.3
radius = 0.0

def deg_2_rad(x) : 
	return 3.141592 * x / 180

def check_pose(pose) :
	if not isinstance(pose, (tuple, list)) : 
		raise TypeError("Expected tuple or list for pose")
	if not all( [isinstance(x, float) for x in pose]) :
		raise TypeError("Expected floats in pose")
	if not len(pose) == 6:
		raise TypeError("Expected 6 members in pose")


def clear_list_tuple(input_data) :
	if not isinstance(input_data, (tuple, list)) : 
		raise TypeError("Expected tuple for pose")
	return str(input_data)[1:-1]




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
	s.connect(ADDR)
except Exception as e:
	print(' %s:%s not connected.' %ADDR)
	sys.exit()
message = 'modbus_add_signal("172.140.17.11", 9, 5, 2, "output1")' + '\n'

s.send(message)

print("complete send")

message = 'modbus_get_signal_status("output1", False)' + '\n'

print(s.send(message))

message = 'modbus_delete_signal("output1")' + '\n'


s.send(message)
message = 'modbus_get_signal_status("output1", False)' + '\n'

print(s.send(message))