# File for the main gamplay loop. . . at least that's what Daniel's using it as for now =_=

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QColor

from ui.colors import *

class GameWindow(QtWidgets.QWidget):
    # Initialization and key functions
    def __init__(
        self,
        teams: list[tuple[str, QColor, QColor]]
    ):
        super().__init__()

        self.setWindowTitle("PHOTON - Game")
        self.resize(720, 643)

        vlayout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Current Game")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        vlayout.addWidget(title)

        curr_scores_label = QtWidgets.QLabel("Current Scores")
        vlayout.addWidget(curr_scores_label)

        leaderboard_hlayout = QHBoxLayout()
        leaderboard_hlayout.setSpacing(0)
        leaderboard_hlayout.setContentsMargins(0, 0, 0, 0)

        self.leaderboard_tables = {
            name: LeaderboardTable(name, primary_color, secondary_color)
            for name, primary_color, secondary_color in teams
        }

        leaderboard_hlayout.addWidget(self.leaderboard_tables["Red Team"])
        leaderboard_hlayout.addWidget(self.leaderboard_tables["Green Team"])

        vlayout.addLayout(leaderboard_hlayout)

        curr_actions_label = QtWidgets.QLabel("Current Game Actions")
        vlayout.addWidget(curr_actions_label)

        self.game_action_table = GameActionTable()
        vlayout.addWidget(self.game_action_table)

        self.setLayout(vlayout)

    def set_team(self, team_name: str, team_data: dict[int, tuple[int, str]]):
        self.leaderboard_tables[team_name].set_team(team_data)

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

        # TODO: implement this!
        # this does nothing yet because we haven't implemented being able to
        # receive game actions!
        total_score_label = QtWidgets.QLabel("Total Score: 0")
        total_score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(total_score_label)

        self.setLayout(layout)

    def set_team(self, team: dict[int, tuple[int, str]]):
        # TODO: map player_id to row in leaderboard
        # fill in team data
        for row, (_, codename) in enumerate(team.values()):
            player_col = self.leaderboard_table.item(2+row, 0)
            score_col  = self.leaderboard_table.item(2+row, 1)

            assert player_col is not None and score_col is not None
            player_col.setText(codename)
            score_col.setText("0")



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
