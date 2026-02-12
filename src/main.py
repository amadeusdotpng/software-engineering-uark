from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose

import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Edit Current Game", alignment=QtCore.Qt.AlignTop)
        self.setWindowTitle("Player Entry Screen")

        self.resize(720, 643)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QLabel("Edit Current Game", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.text)

        self.create_table()

        # Start game button
        self.button = QtWidgets.QPushButton("Start Game")
        self.button.clicked.connect(self.start_game)
        self.layout.addWidget(self.button)


        self.setLayout(self.layout)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)

        # layout.addWidget(self.button)
        # show splash screen when the main window is shown
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('res/splash_screen.jpg').scaled(725, 648)
        label.setPixmap(pixmap)
        label.resize(720, 643)
        label.show()

        # close splash screen after 3 seconds
        QtCore.QTimer.singleShot(300, label.close)

        pass

    #Create table
    def create_table(self):
        self.tableWidget = QTableWidget()
        # self.tableWidget.setSectionResizeMode()
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        #Row count
        self.tableWidget.setRowCount(15)

        #Column count
        self.tableWidget.setColumnCount(6)

        # self.tableWidget.ReadOnlyDelegate()

        self.tableWidget.setItem(0,0, QTableWidgetItem("RED TEAM")) # TODO: lock cells
        self.tableWidget.setItem(0,3, QTableWidgetItem("GREEN TEAM"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("PLAYER ID"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("CODENAME"))
        self.tableWidget.setItem(1,2, QTableWidgetItem("EQUIPMENT ID"))
        self.tableWidget.setItem(1,3, QTableWidgetItem("PLAYER ID"))
        self.tableWidget.setItem(1,4, QTableWidgetItem("CODENAME"))
        self.tableWidget.setItem(1,5, QTableWidgetItem("CODENAME"))

        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.layout.addWidget(self.tableWidget)

    def start_game(self):
        # TODO: actually start the game, currently just ends the program
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow();
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())
