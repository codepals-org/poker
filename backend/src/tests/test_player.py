from dealer.player.player import Player
from names import names

from unittest import TestCase
import unittest.mock as mock
from typing import List

def create_test_players(howmany : int = 8):
    players :List[Player] = []
    for i in range(0,howmany):
        players.append(Player(names[i]))
    return players

class TestPlayer(TestCase):
    def test_creation_variants(self):
        for p in create_test_players():
            assert id(p) == mock.ANY

    def test_check_player_json(self):
        for i, player in enumerate(create_test_players(3)):
            expected_result = {'id': mock.ANY, 'name': names[i],
            'money_seat': 0, 'money_pot': 0, 'role': 'normal',
            'active': False }
            assert player.json() == expected_result