from dealer.model.models import Table, Player
import pytest

from unittest import TestCase
from test_player import create_test_players
import unittest.mock as mock
from typing import List

class PreFlop(TestCase):
    def test_preflop_after_init_4(self) -> Table:
        table = Table() #500 each
        howmany = 8
        players = create_test_players(howmany)
        for player in players:
            table.signup(player)
        table.start_game()
        assert players.current() == players[3] == table.players.active_player()
        assert players.moneypot() == table.big_blind + table.small_blind
        return table

    def test_preflop_everyone_call(self):
        table = self.test_preflop_after_init_4()
        table.players.current().call()
        table.players.current().call()
        table.players.current().call()
        table.players.current().check()
        
        # assert (
        #     table.players[0].money_pot == 
        #     table.players[1].money_pot ==
        #     table.players[2].money_pot ==
        #     table.players[3].money_pot
        #     )