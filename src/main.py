# UI/Rendering imports
from PySide6.QtWidgets import QApplication

from ui.colors import *
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
    teams = [
        ("Red", RED_MAIN_COLOR, RED_SECONDARY_COLOR),
        ("Green", GREEN_MAIN_COLOR, GREEN_SECONDARY_COLOR),
    ]

    photon = PhotonClient(
        database,
        client,
        server,
        teams
    )

    sys.exit(app.exec())
