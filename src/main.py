from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;

import sys

# Team colors
RED_MAIN_COLOR = QtGui.QColor(180, 30, 30)
RED_SECONDARY_COLOR = QtGui.QColor(210, 70, 70)
GREEN_MAIN_COLOR = QtGui.QColor(30, 130, 30)
GREEN_SECONDARY_COLOR = QtGui.QColor(60, 170, 60)
WHITE = QtGui.QColor(255, 255, 255)
DAKRGRAY = QtGui.QColor(60, 60, 60)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PHOTON - Start Screen")
        self.resize(720, 643)

        vlayout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Edit Current Game", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        vlayout.addWidget(title)

        table_hlayout = QHBoxLayout()
        table_hlayout.setSpacing(0)
        table_hlayout.setContentsMargins(0, 0, 0, 0)

        # Player Tables
        self.team_tables = {
            "Red Team": PlayerTable("RED TEAM", RED_MAIN_COLOR, RED_SECONDARY_COLOR),
            "Green Team": PlayerTable("GREEN TEAM", GREEN_MAIN_COLOR, GREEN_SECONDARY_COLOR)
        }
        table_hlayout.addWidget(self.team_tables["Red Team"], 0)
        table_hlayout.addWidget(self.team_tables["Green Team"], 0)
        vlayout.addLayout(table_hlayout)


        buttons_hlayout = QHBoxLayout()

        self.add_player_button = QtWidgets.QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        buttons_hlayout.addWidget(self.add_player_button)

        # Text input field
        # self.input_field = QtWidgets.QLineEdit()
        # self.input_field.setPlaceholderText("ENTER PLAYER ID...")
        # self.input_field.returnPressed.connect(self.enter_id)
        # vlayout.addWidget(self.input_field)

        # Start game button
        self.button = QtWidgets.QPushButton("START GAME")
        self.button.clicked.connect(self.start_game)
        buttons_hlayout.addWidget(self.button)

        vlayout.addLayout(buttons_hlayout)

        # Splash Screen
        # It's important that this is the last one initialized so that it shows up on top of everything.
        pixmap = QtGui.QPixmap("res/splash_screen.jpg").scaled(self.width(), self.height())
        self.splash_screen = QtWidgets.QLabel(self)
        self.splash_screen.setPixmap(pixmap)

        self.setLayout(vlayout)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)
        self.splash_screen.show()

        # close splash screen after 3 seconds
        QtCore.QTimer.singleShot(1000, self.splash_screen.close)

    def resizeEvent(self, event:QtGui.QResizeEvent):
        super().resizeEvent(event)
        if self.splash_screen.isVisible():
            pixmap = self.splash_screen.pixmap().scaled(self.width(), self.height())
            self.splash_screen.setPixmap(pixmap)
            self.splash_screen.resize(self.width(), self.height())

    def start_game(self):
        # TODO: actually start the game, currently just ends the program :P
        self.close()

    def add_player(self, s):
        dlg = AddPlayerDialog(["Red Team", "Green Team"])
        if not dlg.exec():
            return

        player_id, equipment_id, team_name = dlg.get_data()

        assert team_name is not None
        self.team_tables[team_name].add_player(player_id, "Not yet implemented!", equipment_id)

    # def enter_id(self):
    #     text = self.input_field.text()
    #     try:
    #         player_id = int(text)
    #     except ValueError:
    #         print("Invalid player ID: must be an integer")
    #         self.input_field.clear()
    #         return

    #     # TODO: query the database here
    #     # TODO: add option to which team a player should be added
    #     self.red_table.add_player(player_id, "2", "3")
    #     self.green_table.add_player(player_id, "2", "3")
    #     self.input_field.clear()  # Clears the field after pressing enter

class PlayerTable(QtWidgets.QWidget):
    def __init__(self, team_name: str, team_primary_color: QtGui.QColor, team_secondary_color: QtGui.QColor):
        super().__init__()
        self.team_name = team_name
        self.team_primary_color = team_primary_color
        self.team_secondary_color = team_secondary_color
        self.players_num = 0

        layout = QVBoxLayout()

        self.player_table = QTableWidget()
        self.player_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Disable editing of table

        # Set dimensions
        self.player_table.setRowCount(20)
        self.player_table.setColumnCount(3)
        
        # Table will fit the screen horizontally
        self.player_table.horizontalHeader().setStretchLastSection(True)
        self.player_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Hide row/column headers
        self.player_table.verticalHeader().setVisible(False)
        self.player_table.horizontalHeader().setVisible(False)

        # Center the team labels
        table_header = QTableWidgetItem(team_name)
        table_header.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        table_header.setBackground(team_primary_color)
        self.player_table.setItem(0, 0, table_header)
        self.player_table.setSpan(0, 0, 1, 3)

        # Add section headings
        for col, heading in enumerate(['PLAYER ID', 'CODENAME', 'EQUIPMENT ID']):
            item = QTableWidgetItem(heading)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item.setBackground(team_secondary_color)
            self.player_table.setItem(1, col, item)

        layout.addWidget(self.player_table)

        # Fill remaining data cells with gray
        for row in range(2, self.player_table.rowCount()):
            for col in range(6):
                item = QTableWidgetItem()
                item.setBackground(DAKRGRAY)
                item.setForeground(WHITE)
                self.player_table.setItem(row, col, item)

        self.setLayout(layout)

    def add_player(self, player_id, codename, equipment_id):
        if self.player_table.rowCount() - 2 <= self.players_num:
            self.player_table.insertRow(self.player_table.rowCount())

            for col in range(self.player_table.columnCount()):
                item = QTableWidgetItem()
                item.setBackground(DAKRGRAY)
                item.setForeground(WHITE)
                self.player_table.setItem(2 + self.players_num, col, item)

        for col, text in enumerate([player_id, codename, equipment_id]):
            item = self.player_table.item(2 + self.players_num, col)

            assert item is not None
            item.setText(str(text))

        self.players_num += 1

class AddPlayerDialog(QtWidgets.QDialog):
    def __init__(self, team_choices: list[str]):
        super().__init__()

        self.setMinimumWidth(300)
        self.setWindowTitle("Add Player")
        vlayout = QtWidgets.QVBoxLayout(self)

        self.player_id = None
        self.equipment_id = None
        self.team_name = None
        self.team_choices = team_choices

        self.warning_label = QtWidgets.QLabel("Enter the Player and Equipment IDs")
        vlayout.addWidget(self.warning_label)

        self.player_id_field = QtWidgets.QLineEdit()
        self.player_id_field.setPlaceholderText("Enter Player ID...")
        vlayout.addWidget(self.player_id_field)


        self.equipment_id_field = QtWidgets.QLineEdit()
        self.equipment_id_field.setPlaceholderText("Enter Equipment ID...")
        vlayout.addWidget(self.equipment_id_field)


        team_hlayout = QtWidgets.QHBoxLayout()
        self.team_name_label = QtWidgets.QLabel("Team: ")
        team_hlayout.addWidget(self.team_name_label)

        self.team_name_dropdown = QtWidgets.QComboBox()
        self.team_name_dropdown.insertItems(0, team_choices)
        team_hlayout.addWidget(self.team_name_dropdown)

        team_hlayout.addStretch()

        vlayout.addLayout(team_hlayout)

        button_hlayout = QtWidgets.QHBoxLayout()
        button_hlayout.addStretch()

        button = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | 
                QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button.accepted.connect(self.accept)
        button.rejected.connect(self.reject)
        button_hlayout.addWidget(button)

        vlayout.addLayout(button_hlayout)

        self.setLayout(vlayout)

    def accept(self):
        try:
            self.player_id = int(self.player_id_field.text())
            self.equipment_id = int(self.equipment_id_field.text())
            self.team_name = self.team_choices[self.team_name_dropdown.currentIndex()]
        except ValueError:
            self.warning_label.setText("Player ID and Equipment ID must be integers!")
            self.warning_label.setAutoFillBackground(True)
            p = self.warning_label.palette()
            p.setColor(self.warning_label.foregroundRole(), RED_MAIN_COLOR)
            self.warning_label.setPalette(p)
            return

        super().accept()

    def get_data(self) -> tuple[int | None, int | None, str | None]:
        return (self.player_id, self.equipment_id, self.team_name)


class AddCodenameDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow();
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())
