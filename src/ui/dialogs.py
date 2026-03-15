# UI/Rendering imports
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import * # TODO: make verbose; this is bad coding technically ;-;
from PySide6.QtGui import QKeyEvent

from ui.colors import *

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

    def get_data(self):
        return (self.player_id, self.equipment_id, self.team_name)



class AddCodenameDialog(QtWidgets.QDialog):
    def __init__(self, player_id):
        super().__init__()

        self.setMinimumWidth(300)
        self.setWindowTitle("Add Codename")
        vlayout = QtWidgets.QVBoxLayout(self)

        self.codename = None

        self.label = QtWidgets.QLabel(f"Enter a codename for Player '{player_id}' ")
        vlayout.addWidget(self.label)

        self.codename_field = QtWidgets.QLineEdit()
        self.codename_field.setPlaceholderText("Enter Codename...")
        vlayout.addWidget(self.codename_field)

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
        if not self.codename_field.text():
            self.label.setText("Please enter a valid codename!")
            self.label.setAutoFillBackground(True)
            p = self.label.palette()
            p.setColor(self.label.foregroundRole(), RED_MAIN_COLOR)
            self.label.setPalette(p)
            return
        self.codename = self.codename_field.text()
        super().accept()

    def get_data(self):
        return self.codename



class ChangeUDPNetworkDialog(QtWidgets.QDialog):
    # this assumes old_addr is formatted correctly.
    def __init__(self, old_addr):
        super().__init__()

        self.setMaximumWidth(200)
        self.setWindowTitle("Change UDP Network")
        vlayout = QtWidgets.QVBoxLayout(self)

        self.addr = None

        self.label = QtWidgets.QLabel(f"Enter a new IPv4 address")
        vlayout.addWidget(self.label)

        old_addr_vals = old_addr.split('.')
        addr_hlayout = QtWidgets.QHBoxLayout()
        self.addr_fields = [QtWidgets.QLineEdit(text=old_addr_vals[i]) for i in range(4)]
        dot_labels = [QtWidgets.QLabel(".") for _ in range(3)]
        for xs in itertools.zip_longest(self.addr_fields, dot_labels):
            for x in xs:
                if x is None: continue
                addr_hlayout.addWidget(x)

        vlayout.addLayout(addr_hlayout)

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
            addrs = [int(field.text()) for field in self.addr_fields]
            assert all(0 <= v <= 255 for v in addrs)
            self.addr = ".".join(str(v) for v in addrs)
        except Exception:
            self.label.setText("Please use a valid IPv4 address!")
            self.label.setAutoFillBackground(True)
            p = self.label.palette()
            p.setColor(self.label.foregroundRole(), RED_MAIN_COLOR)
            self.label.setPalette(p)
            return

        super().accept()

    def get_data(self):
        return self.addr


