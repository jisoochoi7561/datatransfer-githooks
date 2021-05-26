import socket
import os
import sys
import hashlib

def check_md5_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

file_name = input()
# print("filename is "+ file_name)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("failed to create socket")
    sys.exit()

host = "localhost"
port = 8000

#
# send to sender
s.sendto(("receive "+file_name).encode(),(host,port))
# print("sended message: receive "+file_name)
# "receive " + file_name
#

#
# receiver exist msg

data, addr = s.recvfrom(1024)
receiver_exist_msg=data.decode('utf-8')
# print("received message: "+receiver_exist_msg)

#

#
# if receiver exist msg:
if receiver_exist_msg == 'Exist':

    to_write = open("Received_script.txt", "wb")
    data, addr = s.recvfrom(1024)
    recv_count = int(data.decode('utf-8'))
    # print("recv count: "+str(recv_count))
    while recv_count != 0:
        data, addr = s.recvfrom(1024)
        to_write.write(data)
        recv_count-=1

    to_write.close()
#

#
# file receive ==> open("Received_script.txt", "wb") # Fixed file name
# Receives the standard count for dividing a file from the server
# ==> while recv_count != 0:
# Continuously receive and write file contents
#

#
# file_name.close()
#

# Do not modify the code (below)
rec_md5_hash, addr = s.recvfrom(1024)

if rec_md5_hash.decode('utf8') == check_md5_hash('Received_script.txt'): #
    print("True")
else:
    print("False")
