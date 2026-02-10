# receiver

import socket # same thing just so we can get n stuff

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # yadayada
sock.bind(("", 7500)) # bind is like woah i want allll of da packets on 7500, and thhe empty string is to listen on all networks

print("Wow, I wish Lady Gaga would send a message to me!")

data, addr = sock.recvfrom(1024) # slow down sally wait for a message. we can only get 1024 bytes
print("Got it:", data.decode()) # got the message, then turns it from bytes back to strings