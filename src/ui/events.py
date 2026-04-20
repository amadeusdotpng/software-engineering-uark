from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QHBoxLayout, QLabel

from ui.colors import *

# this is so ultra scuffed but whatever

class PlayerHitEvent(QtWidgets.QWidget):
    def __init__(
        self,
        shooter: tuple[str, QtGui.QColor],
        victim:  tuple[str, QtGui.QColor],
    ):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        shooter_label = QLabel(f'{shooter[0]}')

        shooter_p = shooter_label.palette()
        shooter_p.setColor(shooter_label.foregroundRole(), shooter[1])
        shooter_label.setPalette(shooter_p)

        shooter_f = shooter_label.font()
        shooter_f.setBold(True)
        shooter_label.setFont(shooter_f)

        victim_label = QLabel(f'{victim[0]}')

        victim_p = victim_label.palette()
        victim_p.setColor(victim_label.foregroundRole(), victim[1])
        victim_label.setPalette(victim_p)

        victim_f = victim_label.font()
        victim_f.setBold(True)
        victim_label.setFont(victim_f)

        layout.addWidget(shooter_label)
        layout.addWidget(QLabel(' hit '))
        layout.addWidget(victim_label)

        self.setMaximumHeight(50)

        self.setLayout(layout)

class BaseHitEvent(QtWidgets.QWidget):
    def __init__(
        self,
        shooter:    tuple[str, QtGui.QColor],
        base_color: QtGui.QColor,
    ):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        shooter_label = QLabel(f'{shooter[0]}')

        shooter_p = shooter_label.palette()
        shooter_p.setColor(shooter_label.foregroundRole(), shooter[1])
        shooter_label.setPalette(shooter_p)

        shooter_f = shooter_label.font()
        shooter_f.setBold(True)
        shooter_label.setFont(shooter_f)

        base_label = QLabel(f'Enemy Base')

        base_p = base_label.palette()
        base_p.setColor(base_label.foregroundRole(), base_color)
        base_label.setPalette(base_p)

        base_f = base_label.font()
        base_f.setBold(True)
        base_label.setFont(base_f)

        layout.addWidget(shooter_label)
        layout.addWidget(QLabel(' hit the '))
        layout.addWidget(base_label)

        self.setMaximumHeight(50)
        self.setLayout(layout)
