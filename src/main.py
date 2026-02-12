from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import *

import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Edit Current Game", alignment=QtCore.Qt.AlignTop)
        self.setWindowTitle("Player Entry Screen")

        self.resize(720, 643)
        # self.button = QtWidgets.QPushButton("Click me!")
        # self.text = QtWidgets.QLabel("Hello World",
        #                              alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.createTable()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tableWidget)
        # layout.addWidget(self.text)
        # layout.addWidget(self.button)

        self.setLayout(self.layout)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)

        # show splash screen when the main window is shown
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('res/splash_screen.jpg').scaled(725, 648)
        label.setPixmap(pixmap)
        label.resize(720, 643)
        label.show()

        # close splash screen after 3 seconds
        QtCore.QTimer.singleShot(3000, label.close)

        self.text = QtWidgets.QLabel("Edit Current Game", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.text)
        pass

    #Create table
    def createTable(self):
        self.tableWidget = QTableWidget()

        #Row count
        self.tableWidget.setRowCount(4)

        #Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0,0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("City"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Arnavi"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Mandsaur"))
 
        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow();
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())
