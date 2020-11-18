from dealer.model.table import Table, Phase
from dealer.model.player import Player, PlayerList
import pytest

from unittest import TestCase
from test_player import create_test_players
import unittest.mock as mock
from typing import List

def create_test_tables():
    tables :List[Table] = []
    tables.extend([
        Table(),                        # check default table creation
        Table(500, 10, 20, 10),         # check with integer
        Table(555.55, 10.4, 20.8, 10),  # check with floats
        Table("555","123.3"),           # check with string
    ])
    return tables
class PreGame(TestCase):
    def test_creation_variants(self):
        create_test_tables()
        for t in create_test_tables():
            assert id(t) == mock.ANY

    def test_check_table_json(self):
        expected_result = [
            {
                'id': mock.ANY, 'cash_per_player': 500.0,
                'small_blind': 10.0, 'big_blind': 20.0,
                'phase': Phase.REGISTRATION
            },
            {
                'id': mock.ANY, 'cash_per_player': 500.0,
                'small_blind': 10.0, 'big_blind': 20.0,
                'phase': Phase.REGISTRATION
            },
            {
                'id': mock.ANY, 'cash_per_player': 555.55,
                'small_blind': 10.4, 'big_blind': 20.8,
                'phase': Phase.REGISTRATION
            },
            {
                'id': mock.ANY, 'cash_per_player': 555.0, 
                'small_blind': 123.3, 'big_blind': 20.0,
                'phase': Phase.REGISTRATION
            },
        ]
        for i, table in enumerate(create_test_tables()):
            assert table.json() == expected_result[i]

    def test_too_many_signups_on_table8(self):
        create_test_tables()
        howmany = 10
        test_players = create_test_players(howmany=howmany)
        table = Table() # default 8 seats
        with pytest.raises(RuntimeError) as excinfo:
            for i in range(0,howmany):
                table.signup(test_players[i])
        assert 'Max players reached. No signups anymore.' in str(excinfo.value)

    def test_8_signups(self):
        create_test_tables()
        howmany = 8
        table = Table() # default 8 seats
        test_players = create_test_players(howmany=howmany)
        for i in range(0,howmany):
            table.signup(test_players[i])
        assert len(table.players) == howmany

    def test_max_signups(self):
        create_test_tables()
        howmany = 22
        test_players = create_test_players(howmany=howmany)
        table = Table(max_players=howmany)
        money = 0
        for i in range(0,howmany):
            table.signup(test_players[i])
            money += test_players[i].money_seat
        assert len(table.players) == howmany
        assert money == 500*howmany

    def test_wrong_table_setting23(self):
        with pytest.raises(ValueError) as err:
            Table(max_players=23)
        assert 'Maximum for a Poker Game is is 22 players.' in str(err.value)

    def test_wrong_table_setting_negative(self):
        with pytest.raises(ValueError) as err:
            Table(max_players=-2)
        assert 'Minimum for a Poker Game is 2 players.' in str(err.value)