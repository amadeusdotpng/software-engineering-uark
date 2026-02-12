import socket

# constant variables
DEFAULT_SERVER_ADDRESS  = "127.0.0.1"
BROADCAST_PORT          = 7500
BUFFER_SIZE             = 1024

# changes depending on 
server_address = ""

# create client socket 
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# check for valid input
is_valid_option = False

# asks user if they want to use default server address (127.0.01)
while not is_valid_option: 
    print("Use default server address (", DEFAULT_SERVER_ADDRESS, ")?")
    using_default = input("(y/n): ")

    # validate
    if using_default.lower() != "y" and using_default.lower() != "n" and len(using_default) == 1: 
        print("Invalid option please choose y or n")
        continue
    
    # set server_address to custom or default
    if using_default == "n": 
        server_address = input("Enter server address (#.#.#.#): ")
    else: 
        server_address = DEFAULT_SERVER_ADDRESS

    # create server address port
    server_address_port = (server_address, BROADCAST_PORT)

    # break while loop 
    is_valid_option = True


# asks for equipment id
equipment_id = input("Enter equipment id: ")
encoded_equipment_id = str.encode(equipment_id)

# enable broadcast
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# send equipment id 
print("Sending message to address [", server_address, "] on port [", BROADCAST_PORT, "]")
client_socket.sendto(encoded_equipment_id, server_address_port)
