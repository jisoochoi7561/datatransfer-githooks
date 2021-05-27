import socket
import os
import sys
import hashlib
import struct

def check_md5_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

def check_checksum(rowdata,checksum):
    packet = rowdata[:18]+bytes([0,0])+rowdata[20:]
    i=0
    num = 0
    while i<len(packet):
        if i+1>=len(packet):
            print("There is only one last byte")
            print(format(ord(packet.hex()[i]),"x"))
            num += int(format(ord(packet.hex()[i]),"x"),16)
        else:
            print("first byte")
            print(format(ord(packet.hex()[i]),"x"))
            print("second byte")
            print(format(ord(packet.hex()[i+1]),"x"))
            print("concated bytes")
            print(format(ord(packet.hex()[i]),"x")+format(ord(packet.hex()[i+1]),"x"))
            num += int(format(ord(packet.hex()[i]),"x")+format(ord(packet.hex()[i+1]),"x"),16)
        print("so far, add completed:")
        print(hex(num))
        num = (num>>16) + (num&0xffff);
        print("added carryBit:")
        print(hex(num))
        i+=2
        mask = 0x1111
        num = num^mask
        print("reverse num so that final checksum:")
        print(hex(num))
        b_check_sum = struct.unpack('>H',checksum)
        print("recievd checksum")
        print(hex(b_check_sum))
        print("calculated checksum")
        print(hex(num))
        return rowdata[20:]


file_name = input()
# print("filename is "+ file_name)



host = ("34.64.149.188")
port = 8000

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
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
    checksum, addr = s.recvfrom(1024)
    data, addr = s.recvfrom(1024)
    data = check_checksum(data,checksum)
    recv_count = int(data.decode('utf-8'))
    # print("recv count: "+str(recv_count))
    while recv_count != 0:
        checksum, addr = s.recvfrom(1024)
        data, addr = s.recvfrom(1024)
        data = check_checksum(data,checksum)
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
