import socket
import random
import sys

random_list = [0,1,2]
server_choice = random.choice(random_list)
UDP_IP = "0.0.0.0"
UDP_PORT = 9000

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

data,addr = sock.recvfrom(1024)
client_choice = int(data.decode('utf8'))
result = server_choice - client_choice
if result == 0:
	sock.sendto("Draw.".encode(),addr)
elif result == 1 or result == -2:
	sock.sendto("Win.".encode(),addr)
else:
	sock.sendto("Lose.".encode(),addr)
sys.exit()

