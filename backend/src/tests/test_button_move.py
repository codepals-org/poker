from dealer.table.table import circular_button_move
from dealer.player.player import Player, Role

from unittest import TestCase
from test_player import create_test_players

class TestingButton(TestCase):
    def test_button_move8(self):
        players = create_test_players(8)
        players[0].role = Role.DEALER
        players[1].role = Role.SMALL
        players[2].role = Role.BIG
        circular_button_move(players)
        assert players[0].role == Role.NORMAL
        assert players[1].role == Role.DEALER
        assert players[2].role == Role.SMALL
        assert players[3].role == Role.BIG
        for p in range(4,7):
            assert players[p].role == Role.NORMAL

    def test_button_move3(self):
        players = create_test_players(3)
        players[0].role = Role.DEALER
        players[1].role = Role.SMALL
        players[2].role = Role.BIG
        circular_button_move(players)
        assert players[0].role == Role.BIG
        assert players[1].role == Role.DEALER
        assert players[2].role == Role.SMALL

    def test_button_move2(self):
        players = create_test_players(2)
        players[0].role = Role.SMALL
        players[1].role = Role.BIG
        circular_button_move(players)
        assert players[0].role == Role.BIG
        assert players[1].role == Role.SMALL

    def test_button_move1(self):
        players = create_test_players(1)
        players[0].role = Role.SMALL
        circular_button_move(players)
        assert players[0].role == Role.SMALL