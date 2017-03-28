import time
import socket
import sys

HOST = '192.168.0.11'
PORT = 30003
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

try :
	s.connect(ADDR)
except Exception as e:
	print(' %s:%s not connected.' %ADDR)
	sys.exit()



print('Success connection %s:%s' %ADDR)

angle_start = [90, -95, 90, 0, 90, 90]

angle_start = map(deg_2_rad, angle_start)
cartesian = False

massage = 'socket_open('


massage += '\n'
s.send(massage)
print("Gripp?")

#massage = 'rq_activate'


massage += '\n'
s.send(massage)

time.sleep(2.5)

massage = 'movej({}[{}],a={},v={},r={})'.format('p' if cartesian else '',clear_list_tuple(angle_start), a_joint, v_joint, radius)

massage += '\n'

s.send(massage)
print massage

#time.sleep(2.5)

#angle_finish = [70, -65, 90, 0, 90, 90]
#angle_finish = map(deg_2_rad, angle_finish)

#massage2 = 'movej({}[{}],a={},v={},r={})'.format('p' if cartesian else '',clear_list_tuple(angle_finish), a_joint, v_joint, radius)

#massage2 += '\n'

#time.sleep(2.5)

#s.send(massage2)

#print('test')
