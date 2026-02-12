# sender

import socket # we can create and use sockets with this!

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use an IPv4 address, and use UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # yay we can broadcast (^-^)

broadcast_addy = ("255.255.255.255", 7500) # the 255 add is like woah send it to everyone, and the 7500 is the UDP port

message = "WHAT IF I WAS A SENTIENT MESSAGE?" 
sock.sendto(message.encode(), broadcast_addy) # encode turns the message into bytes to send

print("The message has been sent out to the world, never to be seen again.")

# need: a loop to keep sending messages. prompts to enter specific messages. network selection? 