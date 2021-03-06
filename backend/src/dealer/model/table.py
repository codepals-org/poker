from .player import Player, PlayerList

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

class Phase(Enum):
    REGISTRATION = auto() # Game has not started. Player able to take a seat.
    PREFLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()

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