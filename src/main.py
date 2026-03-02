# UI/Rendering imports
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QKeyEvent

# Custom class imports
from ui import EntryTerminal
from database import PlayerDatabase

# Miscellaneous imports
import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    db = PlayerDatabase()
    window = EntryTerminal(db)
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())
