from dealer.table.table import handout_cards, CARDS
from dealer.player.player import Player, Role
import logging

from unittest import TestCase, mock
from test_player import create_test_players

class TestingHandout(TestCase):
    def test_handout8(self):
        numplayers = 8
        players = create_test_players(numplayers)
        cardstack = CARDS
        handout_cards(players, cardstack)
        for player in players:
            logging.warning(player.hand)
            assert player.hand == [mock.ANY, mock.ANY]
        assert len(cardstack) == 52 - numplayers*2