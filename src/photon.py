from PySide6.QtCore import QObject, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox

from ui import EntryWindow, GameWindow, AddPlayerDialog, AddCodenameDialog, ChangeUDPNetworkDialog
from network import NetSend, NetRecv
from database import PlayerDatabase

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

    def __hash__(self) -> int:
        # recommended implementation according to Python docs
        return hash((self.player_id, self.equipment_id, self.codename))

class PhotonClient(QObject):
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
        self.net_recv = net_recv # TODO: PUT THIS IN A QTHREAD

        self.player_ids: set[int] = set()
        self.equipment_ids: set[int] = set()
        self.teams: dict[str, list[PhotonPlayer]] = {
            name: [] for name, _, _ in teams
        }

        # Timer stuff
        self.countdown_time = 30
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.game_countdown)

        # UI stuff
        self.entry_window = EntryWindow(teams)
        self.entry_window.add_player_signal.connect(self.add_player)
        self.entry_window.clear_players_signal.connect(self.clear_players)
        self.entry_window.change_net_addr_signal.connect(self.change_net_addr)

        self.game_window = GameWindow(teams)

        # show EntryWindow on init
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

    def clear_players(self):
        for team in self.teams.values():
            team.clear()

    def change_net_addr(self):
        dlg = ChangeUDPNetworkDialog(self.net_send.addr)
        if not dlg.exec():
            return
        
        new_addr = dlg.get_data()

        assert new_addr is not None
        self.net_send.set_addr(new_addr)

    def game_countdown(self):
        if self.countdown_time <= 0:
            self.countdown = 30
            self.countdown_timer.stop()
            self.start_game()

    def start_game(self):
        pass
