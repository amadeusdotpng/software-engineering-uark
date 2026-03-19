# Custom class imports
from ui import EntryTerminal, Game
from network import NetSend, NetRecv
from database import PlayerDatabase

class PhotonClient:
    def __init__(
        self,
        database: PlayerDatabase,
        client: NetSend,
        server: NetRecv,
        team_names: list[str],
    ):
        # non-ui stuff / data
        self.database = database
        self.client = client
        self.server = server

        self.player_ids: set[int] = set()
        self.equipment_ids: set[int] = set()
        self.teams: dict[str, list[PhotonPlayer]] = {
            name: [] for name in team_names
        }

        # ui stuff
        self.entry_window = EntryTerminal()
        self.game_window = Game()

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
