import socket
import os
import sys
import hashlib
import math
import struct
host = ("34.64.149.188")
port = 8000

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("0.0.0.0", 8000))
except socket.error:
	print("failed to create socket")
	sys.exit()


def check_md5(path):
	f = open(path, 'rb')
	data = f.read()
	md5_hash = hashlib.md5(data).hexdigest()
	return md5_hash

def cal_check_sum(data):
	src_ip = '192.168.0.4'
	b_src_ip = bytes(map(int, src_ip.split('.')))
	print("b_src_ip")
	print(b_src_ip)

	dst_ip = '192.160.0.2'
	b_dst_ip = bytes(map(int,dst_ip.split('.')))
	print("b_dst_ip")
	print(b_dst_ip)

	zeroes = 0
	b_zeroes = bytes([zeroes])
	print("b_zeroes")
	print(b_zeroes)

	protocol = 17
	b_protocol = bytes([protocol])
	print("b_protocol")
	print(b_protocol)


	b_udp_length = len(data)+8
	print('b_udp_length')
	print(b_udp_length)


	src_port = 8000

	dst_port = 53109

	b_length = b_udp_length

	b_check_sum = bytes([0,0])



	pseudo_header =  b_src_ip+b_dst_ip+b_zeroes+b_protocol+b_udp_length
	print(pseudo_header)
	udp_header = src_port+dst_port+length+check_sum

	packet = pseudo_header+udp_header+data.decode('utf-8')

	return packet.encode('utf-8')
def sender_send(file_name):
	#
	# Implement in the order mentioned in the silde and video.
	if os.path.isfile(file_name):
		s.sendto("Exist".encode('utf-8'), client_addr)
		size = os.stat(file_name).st_size
		check =math.ceil(size / 984)
		check_with_header = cal_check_sum(str(check).encode('utf-8'))
		s.sendto(check_with_header, client_addr)
		read_file = open(file_name, 'rb')
		while check!=0:
			chunk_file = read_file.read(984)
			data_with_header = cal_check_sum(chunk_file)
			s.sendto(data_with_header, client_addr)
			check-=1
		read_file.close()
	else:
		s.sendto("FileNonExistenceError".encode('utf-8'), client_addr)
	#

	# Do not modify the code (below)
	md5_hash = check_md5(file_name)
	s.sendto(md5_hash.encode('utf-8'), client_addr)

if __name__ == "__main__":
	try:
		data, client_addr = s.recvfrom(1024)
	except ConnectionResetError:
		print("error. port number not matching.")
		sys.exit()

	text = data.decode('utf8')
	handler = text.split()

	if handler[0] == 'receive':
		sender_send(handler[1])
