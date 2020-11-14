""" This module defines the player objects and all interactions
a player client can do """
from typing import List

class Player():
    """ The Player is a participant of the Game """
    def __init__(self, name :str):
        self.name :str = str(name)

        self.money_seat :float = float(0)
        self.money_pot :float = float(0)
        self.role :str = 'normal'
        self.active :bool = False

        self.hand :List[str] = []

    def json(self):
        return {
            "id" : id(self),
            "name" : self.name,
            "money_seat": self.money_seat,
            "money_pot" : self.money_pot,
            "role" : self.role,
            "active" : self.active
        }