from dealer.table.table import circular_button_move, init_buttons
from dealer.player.player import Player, Role
import pytest

from unittest import TestCase
from test_player import create_test_players

class TestingButton(TestCase):
    def test_button_init8(self):
        num_players = 8
        players = create_test_players(num_players)
        init_buttons(players)
        assert players[0].role == Role.DEALER
        assert players[1].role == Role.SMALL
        assert players[2].role == Role.BIG
        assert players[3].role == Role.UTG
        for p in range(4,num_players-1):
            assert players[p].role == Role.NORMAL

    def test_button_init3(self):
        num_players = 3
        players = create_test_players(num_players)
        init_buttons(players)
        assert players[0].role == Role.DEALER
        assert players[1].role == Role.SMALL
        assert players[2].role == Role.BIG

    def test_button_init2(self):
        num_players = 2
        players = create_test_players(num_players)
        init_buttons(players)
        assert players[0].role == Role.SMALL
        assert players[1].role == Role.BIG

    def test_button_init1(self):
        num_players = 1
        players = create_test_players(num_players)
        with pytest.raises(ValueError) as err:
            init_buttons(players)
        assert "At least two players needed."

    def test_button_move8(self):
        num_players = 8
        players = create_test_players(num_players)
        players[0].role = Role.DEALER
        players[1].role = Role.SMALL
        players[2].role = Role.BIG
        players[3].role = Role.UTG
        circular_button_move(players)
        assert players[0].role == Role.NORMAL
        assert players[1].role == Role.DEALER
        assert players[2].role == Role.SMALL
        assert players[3].role == Role.BIG
        assert players[4].role == Role.UTG
        for p in range(5,num_players-1):
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