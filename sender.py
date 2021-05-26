import socket
import os
import sys
import hashlib
import math

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("localhost", 8000))
except socket.error:
	print("failed to create socket")
	sys.exit()

def check_md5(path):
	f = open(path, 'rb')
	data = f.read()
	md5_hash = hashlib.md5(data).hexdigest()
	return md5_hash

def sender_send(file_name):
	#
	# Implement in the order mentioned in the silde and video.
	if os.path.isfile(file_name):
		s.sendto("Exist".encode('utf-8'), client_addr)
		size = os.stat(file_name).st_size
		check =math.ceil(size / 4096)
		s.sendto(str(check).encode('utf-8'), client_addr)
		read_file = open(file_name, 'rb')
		while check!=0:
			chunk_file = read_file.read(4096)
			s.sendto(chunk_file, client_addr)
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
		data, client_addr = s.recvfrom(4096)
	except ConnectionResetError:
		print("error. port number not matching.")
		sys.exit()

	text = data.decode('utf8')
	handler = text.split()

	if handler[0] == 'receive':
		sender_send(handler[1])
