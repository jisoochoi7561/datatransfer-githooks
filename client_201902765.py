import socket
import os
import sys
import hashlib
import random

host = ("34.64.149.188")
port = int(9000)

random_list = [0,1,2]
client_choice = random.choice(random_list)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("failed to create socket")
    sys.exit()
s.sendto(str(client_choice).encode(),(host,port))
data, addr = s.recvfrom(2048)
print(data.decode('utf-8'))

sys.exit()
#
# send to sender

# "receive " + file_name
#

#
# receiver exist msg


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

