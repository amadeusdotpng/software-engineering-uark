from PySide6 import QtGui
from PySide6.QtCore import QObject, QTimer, QThread
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox

from network import NetSend, NetRecv
from database import PlayerDatabase

from typing import Iterable

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
    # Change timers to 1 second for testing purposes
    START_GAME_DELAY = 1 # 30 seconds
    GAME_TIMER = 5 # 6 minutes

    def __init__(
        self,
        database: PlayerDatabase,
        net_send: NetSend,
        net_recv: NetRecv,
        team_colors: Iterable[tuple[str, QColor, QColor]],
    ):
        super().__init__()
        # This needs to be here for lazy-loading because otherwise python will
        # complain about circular import bull____. 
        from ui import EntryWindow, GameWindow

        # non-ui stuff / data
        self.database = database
        self.net_send = net_send
        self.net_recv = net_recv
        self.net_recv.recv_data_signal.connect(self.process_recv_data)

        self.net_recv_thread = QThread(parent=self)
        self.net_recv.moveToThread(self.net_recv_thread)
        self.net_recv_thread.started.connect(self.net_recv.recv_data)

        # NOTE: NetRecv thread will be active the entire program's lifetime!!!
        # This means that we could potentially receive data even if a game
        # isn't active.
        # ...i think this is the move but i'm not sure.
        self.net_recv_thread.start() 

        self.team_names = [name for name, _, _ in team_colors]

        self.player_ids: set[int] = set()
        self.players: dict[int, PhotonPlayer] = dict()

        self.game_active = False

        # Countdown timer
        self.countdown_time = PhotonClient.START_GAME_DELAY
        self.countdown_timer = QTimer(interval=1000)
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # Game timer
        self.game_time = PhotonClient.GAME_TIMER
        self.game_timer = QTimer(interval=1000)
        self.game_timer.timeout.connect(self.update_game_timer)

        # UI stuff
        self.entry_window = EntryWindow(team_colors)
        self.entry_window.add_player_signal.connect(self.add_player)
        self.entry_window.clear_players_signal.connect(self.clear_players)
        self.entry_window.change_net_addr_signal.connect(self.change_net_addr)
        self.entry_window.start_game_signal.connect(self.toggle_countdown)
        self.entry_window.close_photon_signal.connect(self.close)

        self.game_window = GameWindow(team_colors)
        self.game_window.close_photon_signal.connect(self.close)

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

    def update_game_timer(self):
        if self.game_time <= 0:
            self.game_time = PhotonClient.GAME_TIMER
            self.game_timer.stop()

            # TODO: Add function to replace text with button to return to entry screen
            return

        self.game_time -= 1
        self.game_window.change_game_timer(self.game_time)

    def start_game(self):
        if self.game_active:
            return
        self.game_active = True

        self.net_send.send_game_start()

        self.game_timer.start()
        self.game_window.change_game_timer(self.game_time)

        self.game_window.update_leaderboards(self.players.values())
        self.entry_window.hide()
        self.game_window.show()


    # TODO: call / connect this to when game ends
    def end_game(self):
        if not self.game_active:
            return
        self.game_active = False

        # TODO: reset all player scores

        self.net_send.send_game_end()

        self.game_window.hide()
        self.entry_window.show()

    # TODO: process data that's received... format is `int:int` where
    # - the first  `int` is the Equipment ID of the person sending the data
    # - the second `int` is the Equipment ID of the person who got shot
    def process_recv_data(self, data: bytes):
        # don't care about received data if game hasn't even started
        if not self.game_active:
            return

        # do stuff... update scores, send equipment id of person who got hit,
        # make sure to check if the person hit a base

    def close(self):
        if self.net_recv_thread.isRunning():
            self.net_recv_thread.requestInterruption()
            self.net_recv_thread.quit()
            self.net_recv_thread.wait()
            print("Shutting down threads...")
