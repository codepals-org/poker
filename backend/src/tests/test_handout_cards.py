from dealer.table.table import CARDS
from dealer.player.player import Player, Role
from dealer.player.playerlist import PlayerList
import logging

from unittest import TestCase, mock
from test_player import create_test_players

class TestingHandout(TestCase):
    def test_handout8(self):
        numplayers = 8
        players :PlayerList= create_test_players(numplayers)
        cardstack = CARDS
        players.handout_cards(cardstack)
        for player in players:
            logging.warning(player.hand)
            assert player.hand == [mock.ANY, mock.ANY]
        assert len(cardstack) == 52 - numplayers*2