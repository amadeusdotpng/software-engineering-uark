from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread
import socket

# sends stuff
class NetSend:
    SEND_PORT = 7500
    def __init__(self, addr="127.0.0.1"):
        self.addr = addr
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def set_addr(self, addr: str):
        # maybe remove this eventually
        print(f"changing network address from {self.addr} to {addr}")
        self.addr = addr

    def send_equipment_id(self, equipment_id):
        # maybe remove this eventually
        print(f"sending Equipment ID '{equipment_id}' to {(self.addr, self.SEND_PORT)}")
        self.sock.sendto(str(equipment_id).encode(), (self.addr, self.SEND_PORT))

    def send_game_start(self):
        print("Game has started, broadcasting code 202")
        self.sock.sendto(str(202).encode(), (self.addr, self.SEND_PORT))

    def send_game_end(self):
        print("Game has ended, broadcasting code 221")
        self.sock.sendto(str(221).encode(), (self.addr, self.SEND_PORT))
        self.sock.sendto(str(221).encode(), (self.addr, self.SEND_PORT))
        self.sock.sendto(str(221).encode(), (self.addr, self.SEND_PORT))

# receives stuff
class NetRecv(QObject):
    RECV_PORT   = 7501
    BUFFER_SIZE = 1024
    ADDR = "0.0.0.0" # receive from any connection

    recv_data_signal = QtCore.Signal(bytes)
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((self.ADDR, self.RECV_PORT))
        self.sock.settimeout(1.0)

    def recv_data(self):
        print('NetRecv active...')
        while not QThread.currentThread().isInterruptionRequested():
            try:
                recv_bytes, _ = self.sock.recvfrom(self.BUFFER_SIZE)
                print(f'emitting bytes: {recv_bytes}')
                self.recv_data_signal.emit(recv_bytes)
            except OSError as e:
                if e.args[0] == 'timed out':
                    continue
                else:
                    print(f'Error in NetRecv: {e}')
            except Exception as e:
                print(f'Error in NetRecv: {e}')
