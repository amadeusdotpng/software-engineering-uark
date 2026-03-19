from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox

from ui import EntryWindow, GameWindow, AddPlayerDialog, AddCodenameDialog
from network import NetSend, NetRecv
from database import PlayerDatabase

class PhotonClient:
    def __init__(
        self,
        database: PlayerDatabase,
        net_send: NetSend,
        net_recv: NetRecv,
        teams: list[tuple[str, QColor, QColor]],
    ):
        # non-ui stuff / data
        self.database = database
        self.net_send = net_send
        self.net_recv = net_recv

        self.player_ids: set[int] = set()
        self.equipment_ids: set[int] = set()
        self.teams: dict[str, list[PhotonPlayer]] = {
            name: [] for name, _, _ in teams
        }

        # UI stuff
        self.entry_window = EntryWindow(teams)
        self.entry_window.add_player_signal.connect(self.add_player)

        self.game_window = GameWindow()

        # Show Entry Window
        self.entry_window.show()

    # TODO: refactor this thing maybe?
    def add_player(self):
        dlg = AddPlayerDialog(list(self.teams.keys()))
        if not dlg.exec():
            return

        player_id, equipment_id, team_name = dlg.get_data()

        # to make my typechecker happy
        assert team_name is not None
        assert player_id is not None
        assert equipment_id is not None

        if player_id in self.player_ids:
            dlg = QMessageBox()
            dlg.setText(f"Player ID '{player_id}' has already been added!")
            dlg.exec()
            return

        if equipment_id in self.equipment_ids:
            dlg = QMessageBox()
            dlg.setText(f"Equipment ID '{equipment_id}' has already been added!")
            dlg.exec()
            return

        if self.database.player_exists(player_id):
            codename = self.database.get_codename(player_id)
        else:
            dlg = AddCodenameDialog(player_id)
            if not dlg.exec(): return
            codename = dlg.get_data()
            self.database.add_player(player_id, codename)

        assert isinstance(codename, str)

        self.teams[team_name].append(PhotonPlayer(player_id, equipment_id, codename))
        self.player_ids.add(player_id)
        self.equipment_ids.add(equipment_id)

        self.net_send.send_equipment_id(equipment_id)

        self.entry_window.add_player(team_name, player_id, equipment_id, codename)

class PhotonPlayer:
    def __init__(
        self,
        player_id: int,
        equipment_id: int,
        codename: str
    ):
        self.player_id    = player_id
        self.equipment_id = equipment_id
        self.codename     = codename

    def data(self) -> tuple[int, int, str]:
        return (self.player_id, self.equipment_id, self.codename)
