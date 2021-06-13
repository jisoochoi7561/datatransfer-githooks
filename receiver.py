import socket
import os
import sys
import hashlib
import struct

ack = 0
host = ("34.64.149.188")
port = 8000
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.settimeout(10);

stu_id = input()
s.sendto(stu_id.encode(),(host,port))


def check_md5_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

def check_checksum(rowdata,checksum):
    print("received: ")
    print(rowdata)
    packet = rowdata[:18]+bytes([0,0])+rowdata[20:]
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
    print("recievd checksum ",end='')
    print(hex(checksum))
    print("calculated checksum ",end='')
    print(hex(num))
    if hex(checksum) != hex(num):
        print("checksum error")
        sys.exit()
    return rowdata[20:]


def stop_and_wait():
    global ack
    try:
        data,addr = s.recvfrom(1024)
        rowdata=data[1:];
        received_data_num=int(data[0]);
        if received_data_num == ack :
            if ack == 0:
                ack = 1
            else: ack =0
            s.sendto(str(ack).encode(), (host, port))
            return True,rowdata
        else:
            s.sendto(str(ack).encode(), (host, port))
            return False,rowdata
    except s.timeout:
        s.sendto('NAK'.encode(),(host,port))
        return stop_and_wait()


to_write = open("Received_script.txt", "wb")
success,checksum = stop_and_wait()
checksum = int(checksum.decode('utf-8'))
success,data = stop_and_wait()
data = check_checksum(data,checksum)
recv_count = int(data.decode('utf-8'))
print("recv_count is ",end = '')
print(recv_count)
print("====================================")
# print("recv count: "+str(recv_count))
while recv_count != 0:
    success,checksum = stop_and_wait()
    checksum = int(checksum.decode('utf-8'))
    if success:
        success,data = stop_and_wait()
        if success:
            to_write_data = check_checksum(data,checksum)
            to_write.write(to_write_data)
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

