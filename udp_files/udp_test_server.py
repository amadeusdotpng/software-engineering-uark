import socket

# constants
LOCAL_IP        = "0.0.0.0"
BROADCAST_PORT  = 7500
BUFFER_SIZE     = 1024

# server socket
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind server ip and port
server_socket.bind((LOCAL_IP, BROADCAST_PORT))

print("UDP server listening on port [", BROADCAST_PORT, "]...")

# listening while loop
while(True):

    # recieve broadcast from client
    recieved_bytes = server_socket.recvfrom(BUFFER_SIZE)
    recieved_msg = recieved_bytes[0].decode('utf-8').replace(" ", "")
    print("Equipment ID: ", recieved_msg.strip()) # message recieved is a list first entry is message
                                             