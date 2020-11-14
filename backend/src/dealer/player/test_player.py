from .player import Player

from unittest import TestCase
import unittest.mock as mock
from typing import List

players :List[Player] = []

class TestPlayer(TestCase):
    def test_creation_variants(self):
        players.extend([
            Player("John Doe"),
            Player("张三"),
            Player("Lieschen Müller")
        ])
        for p in players:
            assert id(p) == mock.ANY

    def test_check_player_json(self):
        expected_result = [
            {
                'id': mock.ANY, 'name': 'John Doe', 'money_seat': 0,
                'money_pot': 0, 'role': 'normal', 'active': False
            },
            {
                'id': mock.ANY, 'name': '张三', 'money_seat': 0,
                'money_pot': 0, 'role': 'normal', 'active': False
            },
            {
                'id': mock.ANY, 'name': 'Lieschen Müller', 'money_seat': 0,
                'money_pot': 0, 'role': 'normal', 'active': False
            },
        ]
        for i, player in enumerate(players):
            assert player.json() == expected_result[i]