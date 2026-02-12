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

        # Text input field
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("Enter player ID...")
        self.input_field.returnPressed.connect(self.on_enter)
        self.layout.addWidget(self.input_field)

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
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Disable editing of table

        # Set dimensions
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(6)

       # Center the team labels
        red_team = QTableWidgetItem("RED TEAM")
        red_team.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.setItem(0, 0, red_team)
        self.tableWidget.setSpan(0, 0, 1, 3)

        green_team = QTableWidgetItem("GREEN TEAM")
        green_team.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.setItem(0, 3, green_team)
        self.tableWidget.setSpan(0, 3, 1, 3)

        # Add section headings
        headings = ["PLAYER ID", "CODENAME", "EQUIPMENT ID", "PLAYER ID", "CODENAME", "CODENAME"]
        for col, heading in enumerate(headings):
            item = QTableWidgetItem(heading)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(1, col, item)

        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.layout.addWidget(self.tableWidget)

        # Hide row/column headers
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

    def start_game(self):
        # TODO: actually start the game, currently just ends the program :P
        self.close()

    def on_enter(self):
        text = self.input_field.text()
        print(f"Entered: {text}")

        # TODO: query the database here

        self.input_field.clear()  # Clears the field after pressing enter

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow();
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())
