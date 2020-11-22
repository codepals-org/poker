from typing import List, TYPE_CHECKING
from enum import Enum, auto
from typing import List
import logging
import collections.abc

if TYPE_CHECKING:
    from .table import Table

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
        self.parent :PlayerList = None

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

class PlayerList(collections.abc.MutableSequence):
    def __init__(self, table :'Table', *args):
        self.table = table
        self.list = list()
        self.extend(list(args))

    def check(self, v):
        if not isinstance(v, Player):
            raise TypeError('item is not of type %s' % Player)

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
        self.list[i].parent = self

    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)
        self.list[i].parent = self

    def __str__(self):
        return str(self.list)
        
    def active_player(self) -> Player:
        for player in self:
            if player.active == True:
                return player
        return None

    def circular_button_move(self) -> None:
        """ moves the each role to the player sitting on the left in case we 
        have two players it will remove the dealer role """
        last_role = self[-1].role
        for position, player in reversed(list(enumerate(self))):
            logging.debug("position: %s role: %s", position, player.role)
            if position == 0:
                player.role = last_role
            else:
                player.role = self[position-1].role
        for position, player in enumerate(self):
            logging.debug("position: %s role: %s", position, player.role)

    def handout_cards(self, cardstack :list) -> None:
        for player in self:
            player.hand.append(cardstack.pop())
        for player in self:
            player.hand.append(cardstack.pop())

    def init_buttons(self) -> None:
        """ In the beginning of the game there are no buttons on each players seat.
        This function gives each player a button-role instead. """
        count = len(self)
        if count <2:
            raise ValueError("At least two players needed.")
        elif count == 2:
            self[0].role = Role.SMALL
            self[1].role = Role.BIG
        elif count > 2:
            self[0].role = Role.DEALER
            self[1].role = Role.SMALL
            self[2].role = Role.BIG
            if count > 3:
                self[3].role = Role.UTG

    def deduct_blinds(self):
        for player in self:
            if player.role == Role.BIG:
                if player.money_seat < self.table.big_blind:
                    player.money_pot = player.money_seat
                    player.money_seat = 0.0
                else:
                    player.money_seat -= self.table.big_blind
                    player.money_pot += self.table.big_blind
            if player.role == Role.SMALL:
                if player.money_seat < self.table.small_blind:
                    player.money_pot = player.money_seat
                    player.money_seat = 0.0
                else:
                    player.money_seat -= self.table.small_blind
                    player.money_pot += self.table.small_blind

    def who_starts(self) -> Player:
        """ Who will start with betting """
        if len(self) > 3:
            starter_role = Role.UTG
        elif len(self) == 3:
            starter_role = Role.DEALER
        elif len(self) == 2:
            starter_role = Role.SMALL
        else:
            raise RuntimeError(
                "It seems like there is not enough players to start")
        for p in self:
            if p.role == starter_role:
                return p

    def current(self) -> Player:
        for p in self:
            if p.active == True: return p
        return None

    def moneypot(self) -> float:
        pot :float = 0
        for p in self:
            pot += p.money_pot
        return pot

    def need_to_pay(self) -> float:
        list_pot = []
        for p in self:
            list_pot.append(p.money_pot)
        return max(list_pot)