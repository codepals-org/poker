""" This are the classes needed for the Poker Game """
from typing import List
from enum import Enum, auto
import random
from typing import List
import logging

CARDS = [
    # Card Abbreviations: 
    # https://commons.wikimedia.org/wiki/Category:SVG_playing_cards
        "2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH",
        "2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD",
        "2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS",
        "2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC"
    ]

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

class Phase(Enum):
    REGISTRATION = auto() # Game has not started. Player able to take a seat.
    PREFLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()

class Role(Enum):
    NORMAL = 0
    DEALER = 1
    SMALL = 2
    BIG = 3
    UTG = 4

class Table():
    """ A Poker Table is where players can participate in a Poker Game """
    def __init__(self, cash_per_player : float = 500,
            small_blind :float = 10, big_blind :float = 20,
            max_players :int = 8):

        if max_players > 22:
            raise ValueError("Maximum for a Poker Game is is 22 players.")

        if max_players < 2:
            raise ValueError("Minimum for a Poker Game is 2 players.")

        self.cash_per_player :float = float(cash_per_player)
        self.small_blind :float = float(small_blind)
        self.big_blind :float = float(big_blind)
        self.max_players :int = int(max_players)

        self.phase :Phase = Phase.REGISTRATION

        self.card_stack :List[str] = CARDS
        random.shuffle(self.card_stack)
        self.players = PlayerList(table=self)
        self.community_cards :List[str] = []

    def json(self):
        return {
            "id" : id(self),
            "cash_per_player": self.cash_per_player,
            "small_blind" : self.small_blind,
            "big_blind" : self.big_blind,
            "phase": self.phase
        }

    def signup(self, player :Player):
        """ A player sits down at the table and gets the start budget"""
        if self.phase != Phase.REGISTRATION:
            raise RuntimeError("Game already started. No signups anymore.")
        if len(self.players) >= self.max_players:
            raise RuntimeError("Max players reached. No signups anymore.")
        else:
            self.players.append(player)
            player.money_seat = self.cash_per_player

    def start_game(self):
        """ Start the game, hand out money to each player """
        if self.phase != Phase.REGISTRATION:
            raise RuntimeError("Game already started.")
        if len(self.players) < 2:
            raise RuntimeError("Not enough players to start the game.")
        self.players.init_buttons()
        self.players.deduct_blinds()
        logging.warning(self.card_stack)
        self.players.handout_cards(self.card_stack)
        self.phase = Phase.PREFLOP
        self.start_preflop()            

    def start_preflop(self):
        self.players.who_starts().active = True

    def call(self):
        self.players.need_to_pay()

class PlayerList(list):
    def __init__(self, table :Table = None):
        super()
        self.table = table

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

