import socket
import os
import sys
import hashlib
import math
import struct


try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("0.0.0.0", 8000))
	buffer_frame_num = '000'
	s.settimeout(10)
except socket.error:
	print("failed to create socket")
	sys.exit()

def stop_and_wait(data,address):
	global buffer_frame_num
	print("sending index:")
	print(buffer_frame_num)
	s.sendto(data,address);
	try:
		received_ack, client_addr = s.recvfrom(1024)
		received_ack = (received_ack.decode('utf-8'))
		print("received_ack:")
		print(received_ack)
		if received_ack == 'NAK':
			print("NAK received: resend")
			stop_and_wait(data,address)
		else:
			print("data transfer succeeded","buffer_frame_num",buffer_frame_num,"received ack",received_ack)
			if buffer_frame_num == '000' and received_ack == '001':
				buffer_frame_num='001'
			elif buffer_frame_num == '001' and received_ack == '000':
				buffer_frame_num = '000'
	except socket.timeout:
		print("time error: resend")
		stop_and_wait(data,address)


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
	udp_header = src_port+dst_port+b_length+b_check_sum
	packet = pseudo_header+udp_header+data
	return num,packet
def sender_send(file_name):
	#
	# Implement in the order mentioned in the silde and video.
	if os.path.isfile(file_name):
		size = os.stat(file_name).st_size
		my_check = math.ceil(size / 981)
		checksum_num,check_with_header = cal_check_sum(str(my_check).encode('utf-8'));
		stop_and_wait(buffer_frame_num.encode()+str(checksum_num).encode('utf-8'), client_addr);
		stop_and_wait(buffer_frame_num.encode()+check_with_header, client_addr)
		read_file = open(file_name, 'rb')
		print("file send started")
		while my_check!=0:
			chunk_file = read_file.read(981)
			checksum_tosend,data_with_header = cal_check_sum(chunk_file);
			stop_and_wait(buffer_frame_num.encode()+str(checksum_tosend).encode('utf-8'), client_addr);
			stop_and_wait(buffer_frame_num.encode() + data_with_header, client_addr)
			my_check-=1
		read_file.close()
		print("file send ended")
	else:
		s.sendto("FileNonExistenceError".encode('utf-8'), client_addr)
	#

	# Do not modify the code (below)

if __name__ == "__main__":
	print("hello world")
	try:
		data, client_addr = s.recvfrom(1024)
	except ConnectionResetError:
		print("error. port number not matching.")
		sys.exit()

	text = data.decode('utf8')

	if text == '201902765':
		print("connection connected")
		sender_send("speech_script.txt")
