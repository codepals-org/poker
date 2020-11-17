from .player import Player

class PlayerList(list):
    def __init__(self):
        super()

    def active_player(self) -> Player:
        for player in self:
            if player.active == True:
                return player
        return None

