# UI/Rendering imports
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QKeyEvent

from ui.colors import *
from ui.dialogs import AddCodenameDialog, AddPlayerDialog, ChangeUDPNetworkDialog
from ui.game import Game

# Database
from database import PlayerDatabase

# Networking
from network import Client, Server


class EntryTerminal(QtWidgets.QWidget):
    # Initialization and key functions
    def __init__(self, db: PlayerDatabase):
        super().__init__()

        self.db = db
        self.client = Client()

        # doesn't need to be used yet!
        # self.server = Server()

        self.teams = {
            "Red Team": {},
            "Green Team": {},
        }

        self.game = Game(self.teams)

        self.setWindowTitle("PHOTON - Start Screen")
        self.resize(720, 643)

        vlayout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Edit Current Game")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
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

        # Add player
        self.add_player_button = QtWidgets.QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        buttons_hlayout.addWidget(self.add_player_button)

        # Clear out player entries
        self.clear_game_button = QtWidgets.QPushButton("Clear Game")
        self.clear_game_button.clicked.connect(self.clear_game)
        buttons_hlayout.addWidget(self.clear_game_button)

        # Change client address
        self.change_udp_network_button = QtWidgets.QPushButton("Change UDP Network")
        self.change_udp_network_button.clicked.connect(self.change_udp_network)
        buttons_hlayout.addWidget(self.change_udp_network_button)

        # Start game button
        self.button = QtWidgets.QPushButton("START GAME")
        self.button.clicked.connect(self.start_game)
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

        # close splash screen after 3 seconds
        QtCore.QTimer.singleShot(3000, self.splash_screen.close)

    # Window functionality
    def newGame(self, checked):
        self.game.show()

    def resizeEvent(self, event:QtGui.QResizeEvent):
        super().resizeEvent(event)
        if self.splash_screen.isVisible():
            pixmap = self.splash_screen.pixmap().scaled(self.width(), self.height())
            self.splash_screen.setPixmap(pixmap)
            self.splash_screen.resize(self.width(), self.height())

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_F5:
            self.start_game()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        super().keyPressEvent(event)

    # Game management
    def start_game(self):
        if self.game.isVisible():
            print("Im doing nothing")
        else:
            self.game.show()
            self.hide()

    def countdown(self):
        # Initialize starting time and timer
        self.countdown = 30
        self.timer = QtCore.QTimer(self)

        # Reduce countdown variable by one every 1000 ms
        self.button.setText(str(self.countdown)+ " seconds until game start...")
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        # Update button text and decrement countdown
        self.countdown = self.countdown - 1
        self.button.setText(str(self.countdown) + " seconds until game start...")

        # Stop timer and start game once 30 seconds have passed
        if self.countdown <= 0:
            self.timer.stop()
            self.start_game()

    # Networking and Database
    def add_player(self):
        dlg = AddPlayerDialog(list(self.team_tables.keys()))
        if not dlg.exec():
            return

        player_id, equipment_id, team_name = dlg.get_data()
        if player_id in self.teams:
            dlg = QtWidgets.QMessageBox()
            dlg.setText(f"Player ID '{player_id}' has already been added!")
            dlg.exec()
            return

        if self.db.player_exists(player_id):
            codename = self.db.get_codename(player_id)
        else:
            dlg = AddCodenameDialog(player_id)
            if not dlg.exec(): return
            codename = dlg.get_data()
            self.db.add_player(player_id, codename)

        assert team_name is not None
        self.teams[team_name][player_id] = (equipment_id, codename)
        self.team_tables[team_name].add_player(player_id, codename, equipment_id)
        self.client.send_equipment_id(equipment_id)

    def change_udp_network(self):
        dlg = ChangeUDPNetworkDialog(self.client.addr)
        if not dlg.exec():
            return

        new_addr = dlg.get_data()
        self.client.set_addr(new_addr)

    def clear_game(self):
        # clears players from the table/screen, but not from the database
        for table in self.team_tables.values(): # for in table
            table.clear_players() # clears
        self.player_equipment_id_map.clear() 

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

    # clears player entries, leaves other stuff
    def clear_players(self): 
        for row in range(2, self.player_table.rowCount()):
            for col in range(self.player_table.columnCount()):
                item = self.player_table.item(row, col)
                if item:
                    item.setText("")
        # resets player count technically
        self.players_num = 0

