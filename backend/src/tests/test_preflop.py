from dealer.table.table import Table, Phase
from dealer.player.player import Player, Role
import pytest

from unittest import TestCase
from test_player import create_test_players
import unittest.mock as mock
from typing import List

class PreFlop(TestCase):
    def preflop_state_4(self):
        table = Table() #500 each
        howmany = 4
        players = create_test_players(howmany)
        for player in players:
            table.signup(player)
        table.start_game()
        active_player = table.players[3].active
        assert  == True
