import socket
import os
import sys
import hashlib
import math
import struct


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
	b_src_ip = struct.pack('>BBBB',192,168,0,4)


	dst_ip = '192.160.0.2'
	b_dst_ip = struct.pack('>BBBB',192,160,0,2)


	zeroes = 0
	b_zeroes = bytes([zeroes])


	protocol = 17
	b_protocol = bytes([protocol])


	print("data length is: ",end = '')
	print(len(data))
	b_udp_length = struct.pack('>H',(len(data)+8))



	src_port = struct.pack('>H',8000)

	dst_port = struct.pack('>H',53109)

	b_length = b_udp_length

	b_check_sum = bytes([0,0])



	pseudo_header =  b_src_ip+b_dst_ip+b_zeroes+b_protocol+b_udp_length
	udp_header = src_port+dst_port+b_length+b_check_sum


	packet = pseudo_header+udp_header+data
	print("packet is",end = '')
	print(packet)

	i=0
	num = 0
	while i<len(packet):
		if i+1>=len(packet):
			num += int(format(ord(packet.hex()[i]),"x"),16)
		else:
			num += int(format(ord(packet.hex()[i]),"x")+format(ord(packet.hex()[i+1]),"x"),16)
		num = (num>>16) + (num&0xffff);
		i+=2
	mask = 0b1111111111111111
	num = num^mask
	print("final checksum: ",end='')
	print(hex(num))
	b_check_sum = struct.pack('>H',num)
	# send checksum
	s.sendto(str(num).encode('utf-8'), client_addr)
	udp_header = src_port+dst_port+b_length+b_check_sum
	packet = pseudo_header+udp_header+data
	return packet
def sender_send(file_name):
	#
	# Implement in the order mentioned in the silde and video.
	frame_num = 0
	if os.path.isfile(file_name):
		s.sendto("Exist".encode('utf-8'), client_addr)
		size = os.stat(file_name).st_size
		check =math.ceil(size / 984)
		check_with_header = cal_check_sum(str(check).encode('utf-8'))
		print("check send started: ",end='')
		print(check)
		s.sendto(check_with_header, client_addr)
		print("check send ended")
		read_file = open(file_name, 'rb')
		print("file send started")
		while check!=0:
			chunk_file = read_file.read(984)
			data_with_header = cal_check_sum(chunk_file)
			s.sendto(data_with_header, client_addr)
			check-=1
		read_file.close()
		print("file send ended")
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
