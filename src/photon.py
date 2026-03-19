# Custom class imports
from ui import EntryWindow, GameWindow
from network import NetSend, NetRecv
from database import PlayerDatabase

class PhotonClient:
    def __init__(
        self,
        database: PlayerDatabase,
        net_send: NetSend,
        net_recv: NetRecv,
        team_names: list[str],
    ):
        # non-ui stuff / data
        self.database = database
        self.net_send = net_send
        self.net_recv = net_recv

        self.player_ids: set[int] = set()
        self.equipment_ids: set[int] = set()
        self.teams: dict[str, list[PhotonPlayer]] = {
            name: [] for name in team_names
        }

        # ui stuff
        self.entry_window = EntryWindow()
        self.game_window = GameWindow()

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
