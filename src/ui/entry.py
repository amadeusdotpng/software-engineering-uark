# UI/Rendering imports
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QKeyEvent, QColor

from ui.colors import *

from typing import Iterable

class EntryWindow(QtWidgets.QWidget):
    add_player_signal = QtCore.Signal()
    clear_players_signal = QtCore.Signal()
    change_net_addr_signal = QtCore.Signal()
    start_game_signal = QtCore.Signal()
    close_photon_signal = QtCore.Signal()

    def __init__(
        self,
        teams: Iterable[tuple[str, QColor, QColor]]
    ):
        super().__init__()

        self.setWindowTitle("PHOTON - Start Screen")
        self.resize(720, 643)

        vlayout = QtWidgets.QVBoxLayout(self)

        # Title
        title = QtWidgets.QLabel("Edit Current Game")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        vlayout.addWidget(title)

        # Player Tables
        table_hlayout = QHBoxLayout()
        table_hlayout.setSpacing(0)
        table_hlayout.setContentsMargins(0, 0, 0, 0)

        self.team_tables = {
            name: PlayerTable(name.upper(), primary, secondary)
            for name, primary, secondary in teams
        }

        for table in self.team_tables.values():
            table_hlayout.addWidget(table, 0)
        vlayout.addLayout(table_hlayout)

        # Buttons
        buttons_hlayout = QHBoxLayout()

        # Add player
        self.add_player_button = QtWidgets.QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player_signal.emit)
        buttons_hlayout.addWidget(self.add_player_button)

        # Clear out player entries
        self.clear_players_button = QtWidgets.QPushButton("Clear Game")
        # For `PhotonClient` to clear data
        self.clear_players_button.clicked.connect(self.clear_players_signal.emit)
        # Clear players on the UI
        self.clear_players_button.clicked.connect(self.clear_players) 

        buttons_hlayout.addWidget(self.clear_players_button)

        # Change client address
        self.change_net_addr_button = QtWidgets.QPushButton("Change UDP Network")
        self.change_net_addr_button.clicked.connect(self.change_net_addr_signal)
        buttons_hlayout.addWidget(self.change_net_addr_button)

        # Start game button
        self.button = QtWidgets.QPushButton("Start Game")
        self.button.clicked.connect(self.start_game_signal.emit)
        buttons_hlayout.addWidget(self.button)

        vlayout.addLayout(buttons_hlayout)

        # Splash Screen
        # It's important that this is the last one initialized so that it shows up on top of everything.
        pixmap = QtGui.QPixmap("res/splash_screen.jpg").scaled(self.width(), self.height())
        self.splash_screen = QtWidgets.QLabel(self)
        self.splash_screen.resize(self.width(), self.height())
        self.splash_screen.setPixmap(pixmap)

        self.setLayout(vlayout)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)
        self.splash_screen.show()

        self.splash_screen.close()
        # close splash screen after 3 seconds
        QtCore.QTimer.singleShot(3000, self.splash_screen.hide)

    def closeEvent(self, event: QtGui.QCloseEvent):
        super().closeEvent(event)
        self.close_photon_signal.emit()

    def resizeEvent(self, event:QtGui.QResizeEvent):
        super().resizeEvent(event)
        if self.splash_screen.isVisible():
            pixmap = self.splash_screen.pixmap().scaled(self.width(), self.height())
            self.splash_screen.setPixmap(pixmap)
            self.splash_screen.resize(self.width(), self.height())

    # def keyPressEvent(self, event: QtGui.QKeyEvent):
    #     if event.key() == QtCore.Qt.Key.Key_F5:
    #         self.start_game()
    #     super().keyPressEvent(event)

    # This assumes that the player has been validated, i.e. the player has a valid player id, a
    # valid equipment id, a valid codename, and is a not a duplicate.
    def add_player(self, team_name: str, player_id: int, equipment_id: int, codename: str):
        self.team_tables[team_name].add_player(player_id, equipment_id, codename)

    def clear_players(self):
        # clears players from the table/screen, but not from the database
        for table in self.team_tables.values(): # for in table
            table.clear_players() # clears

    def change_countdown_text(self, n: int):
        self.button.setText(f'{n} seconds until game start...')

    def reset_countdown_text(self):
        self.button.setText('Start Game')


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
        self.player_table.setRowCount(22)
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
            for col in range(self.player_table.columnCount()):
                item = QTableWidgetItem()
                item.setBackground(DARKGRAY)
                item.setForeground(WHITE)
                self.player_table.setItem(row, col, item)

        self.setLayout(layout)

    def add_player(self, player_id: int, equipment_id: int, codename: str):
        if self.player_table.rowCount() - 2 <= self.players_num:
            self.player_table.insertRow(self.player_table.rowCount())

            for col in range(self.player_table.columnCount()):
                item = QTableWidgetItem()
                item.setBackground(DARKGRAY)
                item.setForeground(WHITE)
                self.player_table.setItem(2 + self.players_num, col, item)

        # Reordered from argument list
        for col, text in enumerate([player_id, codename, equipment_id]):
            item = self.player_table.item(2 + self.players_num, col)

            # to make my typehecker happy
            assert item is not None
            item.setText(str(text))

        self.players_num += 1

    # clears player entries, leaves other stuff
    def clear_players(self): 
        for row in range(2, self.player_table.rowCount()):
            for col in range(self.player_table.columnCount()):
                item = self.player_table.item(row, col)
                if item:
                    item.setText("")
        # resets player count technically
        self.players_num = 0


