# UI/Rendering imports
from PySide6.QtWidgets import QApplication

from network import NetSend, NetRecv
from database import PlayerDatabase
from photon import PhotonClient

# Miscellaneous imports
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    database = PlayerDatabase()
    client = NetSend()
    server = NetRecv()

    photon = PhotonClient(
        database,
        client,
        server,
        ["Red", "Green"]
    )

    sys.exit(app.exec())
