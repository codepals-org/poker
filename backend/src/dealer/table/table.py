""" This are the classes needed for the Poker Game """
from typing import List
from enum import Enum, auto
from dealer.player.player import Player

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

        self.players :List[Player] = []
        self.community_cards :List[str] = []

    def json(self):
        return {
            "id" : id(self),
            "cash_per_player": self.cash_per_player,
            "small_blind" : self.small_blind,
            "big_blind" : self.big_blind,
            "phase": self.phase
        }

    def start_game(self):
        """ Start the game, hand out money to each player """
        if self.phase != Phase.REGISTRATION:
            raise RuntimeError("Game already started.")
        self.game_started = True

    def signup(self, player :Player):
        """ A player sits down at the table and gets the start budget"""
        if self.phase != Phase.REGISTRATION:
            raise RuntimeError("Game already started. No signups anymore.")
        if len(self.players) >= self.max_players:
            raise RuntimeError("Max players reached. No signups anymore.")
        else:
            self.players.append(player)
            player.money_seat = self.cash_per_player


