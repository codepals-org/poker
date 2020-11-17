""" This module defines the player objects and all interactions
a player client can do """
from typing import List
from enum import Enum

class Role(Enum):
    NORMAL = 0
    DEALER = 1
    SMALL = 2
    BIG = 3
    UTG = 4

class Player():
    """ The Player is a participant of the Game """
    def __init__(self, name :str):
        self.name :str = str(name)

        self.money_seat :float = float(0)
        self.money_pot :float = float(0)
        self.role :str = Role.NORMAL
        self.active :bool = False

        self.hand :List[str] = []
        self.bet_counter = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def json(self):
        return {
            "id" : id(self),
            "name" : self.name,
            "money_seat": self.money_seat,
            "money_pot" : self.money_pot,
            "role" : self.role,
            "active" : self.active,
            "bet_counter" : self.bet_counter, # players allowed to bet 4 times
        }

    def call(self):
        pass

    def check(self):
        pass