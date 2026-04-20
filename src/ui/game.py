# File for the main gamplay loop. . . at least that's what Daniel's using it as for now =_=

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QColor, QIcon

from ui.colors import *
from ui.events import PlayerHitEvent, BaseHitEvent
from photon import PhotonPlayer

from typing import Iterable
import itertools

# TODO: a way to end game early?
# TODO: add base icon to player who hit a base
class GameWindow(QtWidgets.QWidget):
    close_photon_signal = QtCore.Signal()
    end_game_signal = QtCore.Signal()

    # Initialization and key functions
    def __init__(
        self,
        team_colors: Iterable[tuple[str, QColor, QColor]]
    ):
        super().__init__()

        self.setWindowTitle("PHOTON - Game")
        self.resize(720, 643)

        self.top_team  = None
        self.top_score = 0
        vlayout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Current Game")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        vlayout.addWidget(title)

        scores_label = QtWidgets.QLabel("Current Scores")
        vlayout.addWidget(scores_label)

        leaderboard_hlayout = QHBoxLayout()
        leaderboard_hlayout.setSpacing(0)
        leaderboard_hlayout.setContentsMargins(0, 0, 0, 0)

        self.leaderboard_tables = {
            name: LeaderboardTable(name.upper(), primary_color, secondary_color)
            for name, primary_color, secondary_color in team_colors
        }

        for table in self.leaderboard_tables.values():
            leaderboard_hlayout.addWidget(table)

        vlayout.addLayout(leaderboard_hlayout)

        curr_actions_label = QtWidgets.QLabel("Current Game Actions")
        vlayout.addWidget(curr_actions_label)

        self.events_table = EventsTable()
        vlayout.addWidget(self.events_table)

        self.game_timer = QtWidgets.QLabel("Time Remaining: 6:00")
        self.game_timer.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.game_timer.setStyleSheet("font-size: 14pt;")
        vlayout.addWidget(self.game_timer)

        self.return_button = QtWidgets.QPushButton("Return to Player Entry")
        self.return_button.clicked.connect(self.end_game_signal.emit)
        vlayout.addWidget(self.return_button)

        self.setLayout(vlayout)

    def change_game_timer(self, n: int):
        minutes = int(n / 60)
        seconds = n % 60

        if seconds > 9:
            self.game_timer.setText(f"Time Remaining: {minutes}:{seconds}")
        else:
            self.game_timer.setText(f"Time Remaining: {minutes}:0{seconds}")

    def update_timer_status(self, game_active):
        if game_active:
            self.game_timer.show()
            self.return_button.hide()
        else:
            self.game_timer.hide()
            self.return_button.show()

    def update_leaderboards(self, all_players: Iterable[PhotonPlayer]):
        # passes in all players that belong to a team to their respective
        # leaderboard.
        scores: list[tuple[str, int]] = []
        for team, players in itertools.groupby(all_players, lambda p: p.team):
            # original iterator gets consumed after iterating through it once :)
            # must store in a new list
            players = list(players) 
            self.leaderboard_tables[team].update_leaderboard(
                [(p.codename, p.hit_base, p.score) for p in players]
            )
            scores.append((team, sum(p.score for p in players)))

        # leaderboard header flashes if the leading team changes
        top_team, top_score = max(scores, key=lambda e: e[1])
        if self.top_team != top_team and top_score > self.top_score and top_score > 0:
            self.top_team = top_team
            self.leaderboard_tables[self.top_team].flash()


    def push_event(self, event):
        self.events_table.add_event(event)

    def closeEvent(self, event: QtGui.QCloseEvent):
        super().closeEvent(event)
        self.close_photon_signal.emit()


class LeaderboardTable(QtWidgets.QWidget):
    def __init__(
        self,
        team_name: str,
        team_primary_color: QtGui.QColor,
        team_secondary_color: QtGui.QColor,
    ):
        super().__init__()
        self.team_name = team_name
        self.team_primary_color = team_primary_color
        self.team_secondary_color = team_secondary_color

        layout = QVBoxLayout()

        self.leaderboard_table = QTableWidget()
        self.leaderboard_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Disable editing of table

        # set dimensions
        self.leaderboard_table.setRowCount(12)
        self.leaderboard_table.setColumnCount(2)

        # table will fit the screen horizontally
        self.leaderboard_table.horizontalHeader().setStretchLastSection(True)
        self.leaderboard_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # hide row/column headers
        self.leaderboard_table.verticalHeader().setVisible(False)
        self.leaderboard_table.horizontalHeader().setVisible(False)

        # center team labels
        table_header = QTableWidgetItem(team_name)
        table_header.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        table_header.setBackground(team_primary_color)
        self.leaderboard_table.setItem(0, 0, table_header)
        self.leaderboard_table.setSpan(0, 0, 1, 2)

        # add section headings
        for col, heading in enumerate(['PLAYER', 'SCORE']):
            item = QTableWidgetItem(heading)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item.setBackground(team_secondary_color)
            self.leaderboard_table.setItem(1, col, item)

        # fill remaining data cells with gray
        for row in range(2, self.leaderboard_table.rowCount()):
            for col in range(self.leaderboard_table.columnCount()):
                item = QTableWidgetItem()
                item.setBackground(DARKGRAY)
                item.setForeground(WHITE)
                self.leaderboard_table.setItem(row, col, item)

        layout.addWidget(self.leaderboard_table)

        self.total_score_label = QtWidgets.QLabel("Total Score: 0")
        self.total_score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.total_score_label)

        self.setLayout(layout)

    def update_leaderboard(self, player_scores: Iterable[tuple[str, bool, int]]):
        sorted_scores = sorted(player_scores, key=lambda x: x[1], reverse=True)
        total = 0

        for i, (codename, hit_base, score) in enumerate(sorted_scores):
            row = 2 + i
            player_item = self.leaderboard_table.item(row, 0)
            assert player_item is not None
            player_item.setText(codename)
            if hit_base:
                player_item.setIcon(QIcon('res/baseicon.jpg'))
            else:
                player_item.setIcon(QIcon())

            item = self.leaderboard_table.item(row, 1)
            assert item is not None
            item.setText(str(score))

            total += score

        self.total_score_label.setText(f"Total Score: {total}")


    def flash(self):
        original = self.leaderboard_table.item(0, 0).background().color()
        self.leaderboard_table.item(0, 0).setBackground(WHITE)
        QtCore.QTimer.singleShot(300, lambda: self.leaderboard_table.item(0, 0).setBackground(original))


class EventsTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.events_container_widget = QWidget()

        self.events_container = QVBoxLayout()
        self.events_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.events_container.setSpacing(1)
        self.events_container.setContentsMargins(0, 0, 0, 0)


        self.events_container_widget.setLayout(self.events_container)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)

        scroll.setWidget(self.events_container_widget)


        p = self.events_container_widget.palette()
        p.setColor(self.events_container_widget.backgroundRole(), LIGHTGRAY)
        self.events_container_widget.setPalette(p)

        layout.addWidget(scroll)

        self.setLayout(layout)


    def add_event(self, event):
        self.events_container.insertWidget(0, event)
