# UI/Rendering imports
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QKeyEvent

# Custom class imports
from ui import EntryTerminal, Game
from network import NetSend, NetRecv
from database import PlayerDatabase

# Miscellaneous imports
import sys

class PhotonClient:
    def __init__(
        self,
        database: PlayerDatabase,
        client: NetSend,
        server: NetRecv
    ):
        self.database = database
        self.client = client
        self.server = server

        self.entry_window = EntryTerminal()
        self.game_window = Game()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    database = PlayerDatabase()
    client = NetSend()
    server = NetRecv()

    photon = PhotonClient(
        database,
        client,
        server
    )

    sys.exit(app.exec())
