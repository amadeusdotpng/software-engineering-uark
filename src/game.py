# File for the main gamplay loop. . . at least that's what Daniel's using it as for now =_=

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QKeyEvent

import sys
import itertools

class Game(QtWidgets.QWidget):
    # Initialization and key functions
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PHOTON - Game")
        self.resize(720, 643)

        vlayout = QtWidgets.QVBoxLayout(self)

        table_hlayout = QHBoxLayout()
        table_hlayout.setSpacing(0)
        table_hlayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vlayout)

        print("Game initialized")
