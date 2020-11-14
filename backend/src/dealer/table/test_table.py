from .table import Table

from unittest import TestCase
import unittest.mock as mock
from typing import List

tables :List[Table] = []

class PreGame(TestCase):
    def test_creation_variants(self):
        tables.extend([
            Table(),                        # check default table creation
            Table(500, 10, 20, 10),         # check with integer
            Table(555.55, 10.4, 20.8, 10),  # check with floats
            Table("555","123.3"),           # check with string
        ])
        for t in tables:
            assert id(t) == mock.ANY

    def test_check_table_json(self):
        expected_result = [
            {
                'id': mock.ANY, 'cash_per_player': 500.0,
                'small_blind': 10.0, 'big_blind': 20.0, 'game_started': False,
                'round_started': False},
            {
                'id': mock.ANY, 'cash_per_player': 500.0,
                'small_blind': 10.0, 'big_blind': 20.0, 'game_started': False,
                'round_started': False}, 
            {
                'id': mock.ANY, 'cash_per_player': 555.55,
                'small_blind': 10.4, 'big_blind': 20.8, 'game_started': False,
                'round_started': False},
            {
                'id': mock.ANY, 'cash_per_player': 555.0, 'small_blind': 123.3,
                'big_blind': 20.0, 'game_started': False,
                'round_started': False
            },
        ]
        for i, table in enumerate(tables):
            assert table.json() == expected_result[i]