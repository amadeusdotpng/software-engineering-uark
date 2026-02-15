import socket


# sends stuff
class Client:
    SEND_PORT = 7500
    def __init__(self, addr="127.0.0.1"):
        self.addr = addr
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def set_addr(self, addr):
        # maybe remove this eventually
        print(f"changing network address from {self.addr} to {addr}")
        self.addr = addr

    def send_equipment_id(self, equipment_id):
        # maybe remove this eventually
        print(f"sending Equipment ID '{equipment_id}' to {(self.addr, self.SEND_PORT)}")
        self.sock.sendto(str(equipment_id).encode(), (self.addr, self.SEND_PORT))

# receives stuff
class Server:
    RECV_PORT   = 7501
    BUFFER_SIZE = 1024
    ADDR = "0.0.0.0" # receive from any connection
    def __init__(self):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((self.ADDR, self.RECV_PORT))

    # TODO: receive and properly parse data. we don't need to do this for Sprint 2.
    # This is blocking, so we will have to put this on a QThread thing.
    def recv_data(self):
        recv_bytes, _ = self.sock.recvfrom(self.BUFFER_SIZE)
        return int(recv_bytes.decode().strip())
