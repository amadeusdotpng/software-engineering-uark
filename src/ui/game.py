# File for the main gamplay loop. . . at least that's what Daniel's using it as for now =_=

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QColor

from ui.colors import *
from photon import PhotonPlayer

from typing import Iterable
import itertools

# TODO: a way to end game early?
# TODO: add base icon to player who hit a base
class GameWindow(QtWidgets.QWidget):
    close_photon_signal = QtCore.Signal()
    end_game_signal = QtCore.Signal()
    # DEBUG ONLY - remove before release
    debug_key_signal = QtCore.Signal(str)

    # Initialization and key functions
    def __init__(
        self,
        team_colors: Iterable[tuple[str, QColor, QColor]]
    ):
        super().__init__()

        self.setWindowTitle("PHOTON - Game")
        self.resize(720, 643)

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

        self.game_action_table = GameActionTable()
        vlayout.addWidget(self.game_action_table)

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
        team_totals: dict[str, int] = {}
        for team, players in itertools.groupby(all_players, lambda p: p.team):
            player_scores = [(p.codename, p.score) for p in players]
            self.leaderboard_tables[team].update_leaderboard(player_scores)
            team_totals[team] = sum(score for _, score in player_scores)

        if team_totals:
            leading_team = max(team_totals, key=lambda t: team_totals[t])
            self.leaderboard_tables[leading_team].flash_header()

    def closeEvent(self, event: QtGui.QCloseEvent):
        super().closeEvent(event)
        self.close_photon_signal.emit()

    # DEBUG ONLY - remove before release
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_A:
            self.debug_key_signal.emit("a")
        elif event.key() == QtCore.Qt.Key.Key_B:
            self.debug_key_signal.emit("b")
        else:
            super().keyPressEvent(event)



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
                item.setBackground(DAKRGRAY)
                item.setForeground(WHITE)
                self.leaderboard_table.setItem(row, col, item)

        layout.addWidget(self.leaderboard_table)

        self.total_score_label = QtWidgets.QLabel("Total Score: 0")
        self.total_score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.total_score_label)

        self.setLayout(layout)

    # This method assumes that all of the players in player_scores belong in
    # this team's leaderboard.
    def update_leaderboard(self, player_scores: Iterable[tuple[str, int]]):
        sorted_scores = sorted(player_scores, key=lambda x: x[1], reverse=True)

        for i, (name, score) in enumerate(sorted_scores):
            row = i + 2  # rows 0 and 1 are the header and column labels
            if row >= self.leaderboard_table.rowCount():
                break

            name_item = self.leaderboard_table.item(row, 0)
            score_item = self.leaderboard_table.item(row, 1)

            name_item.setText(name)
            score_item.setText(str(score))

        total = sum(score for _, score in sorted_scores)
        self.total_score_label.setText(f"Total Score: {total}")

    def flash_header(self):
        """Flash the team header to highlight the leading team."""
        header_item = self.leaderboard_table.item(0, 0)
        original_color = self.team_primary_color
        flash_color = QColor("yellow")
        flash_count = [0]
        MAX_FLASHES = 6  # 3 on/off cycles

        def toggle_flash():
            if flash_count[0] >= MAX_FLASHES:
                header_item.setBackground(original_color)
                flash_timer.stop()
                return
            header_item.setBackground(flash_color if flash_count[0] % 2 == 0 else original_color)
            flash_count[0] += 1

        flash_timer = QtCore.QTimer(self)
        flash_timer.setInterval(300)
        flash_timer.timeout.connect(toggle_flash)
        flash_timer.start()


# TODO: implement this!
# this does nothing yet because we haven't implemented being able to receive
# game actions!
class GameActionTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        none_label = QtWidgets.QLabel("No Game Actions yet!")
        none_label.setMinimumHeight(200)
        layout.addWidget(none_label)

        self.setLayout(layout)
