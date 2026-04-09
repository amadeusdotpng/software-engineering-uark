from PySide6.QtCore import QObject, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox

from network import NetSend, NetRecv
from database import PlayerDatabase

class PhotonPlayer:
    def __init__(
        self,
        player_id: int,
        codename: str,
        team: str
    ):
        self.player_id = player_id
        self.codename  = codename
        self.team      = team
        self.score     = 0

    def data(self) -> tuple[int, str, str]:
        return (self.player_id, self.codename, self.team)

    def __hash__(self) -> int:
        # recommended implementation according to Python docs
        return hash((self.player_id, self.codename, self.team))

class PhotonClient(QObject):
    START_GAME_DELAY = 5 # 30 seconds

    def __init__(
        self,
        database: PlayerDatabase,
        net_send: NetSend,
        net_recv: NetRecv,
        teams: list[tuple[str, QColor, QColor]],
    ):
        # This needs to be here for lazy-loading because otherwise python will
        # complain about circular import bull____. 
        from ui import EntryWindow, GameWindow

        # non-ui stuff / data
        self.database = database
        self.net_send = net_send
        self.net_recv = net_recv # TODO: PUT THIS IN A QTHREAD

        self.team_names = [name for name, _, _ in teams]

        self.player_ids: set[int] = set()
        self.players: dict[int, PhotonPlayer] = dict()


        # Timer stuff
        self.countdown_time = PhotonClient.START_GAME_DELAY
        self.countdown_timer = QTimer(interval=1000)
        self.countdown_timer.timeout.connect(self.update_countdown)
        # TODO: ADD TIMER FOR GAME

        # UI stuff
        self.entry_window = EntryWindow(teams)
        self.entry_window.add_player_signal.connect(self.add_player)
        self.entry_window.clear_players_signal.connect(self.clear_players)
        self.entry_window.change_net_addr_signal.connect(self.change_net_addr)
        self.entry_window.start_game_signal.connect(self.toggle_countdown)

        self.game_window = GameWindow(teams)

        # show EntryWindow on init
        self.entry_window.show()

    def add_player(self):
        # read top comment of __init__
        from ui import AddPlayerDialog, AddCodenameDialog

        dlg = AddPlayerDialog(self.team_names)
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

        if equipment_id in self.players:
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

        self.players[equipment_id] = PhotonPlayer(player_id, codename, team_name)
        self.player_ids.add(player_id)

        self.net_send.send_equipment_id(equipment_id)

        self.entry_window.add_player(team_name, player_id, equipment_id, codename)

    def clear_players(self):
        self.players.clear()

    def change_net_addr(self):
        # read top comment of __init__
        from ui import ChangeUDPNetworkDialog
        dlg = ChangeUDPNetworkDialog(self.net_send.addr)
        if not dlg.exec():
            return
        
        new_addr = dlg.get_data()

        assert new_addr is not None
        self.net_send.set_addr(new_addr)

    def toggle_countdown(self):
        if self.countdown_timer.isActive():
            self.countdown_time = PhotonClient.START_GAME_DELAY
            self.countdown_timer.stop()

            self.entry_window.reset_countdown_text()
            return

        self.countdown_timer.start()
        self.entry_window.change_countdown_text(self.countdown_time)

    def update_countdown(self):
        if self.countdown_time <= 0:
            self.countdown_time = PhotonClient.START_GAME_DELAY
            self.countdown_timer.stop()

            self.entry_window.reset_countdown_text()
            self.start_game()
            return

        self.countdown_time -= 1
        self.entry_window.change_countdown_text(self.countdown_time)

    def start_game(self):
        self.net_send.send_game_start()

        self.game_window.update_leaderboards(self.players.values())

        self.entry_window.hide()
        self.game_window.show()

    # TODO: call / connect this to when game ends
    def end_game(self):
        self.net_send.send_game_end()

        self.game_window.hide()
        self.entry_window.show()
