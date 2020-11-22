from dealer.model.player import PlayerList, Player, Role
from dealer.model.table import Table
from names import names

from unittest import TestCase
import unittest.mock as mock
from typing import List

def create_test_players(howmany : int = 8) -> PlayerList:
    players = PlayerList(Table())
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
            'money_seat': 0, 'money_pot': 0, 'role': Role.NORMAL,
            'active': False, 'bet_counter': 0 }
            assert player.json() == expected_result

class TestPlayerList(TestCase):
    def test_append(self):
        playerlist = create_test_players(20)
        list = []
        playerlist2 = PlayerList(Table())
        for p in playerlist:
            list.append(p) # list is a normal list, no effect on p.parent
            assert p.parent == playerlist
            playerlist2.append(p) ## parent list should change for elements
            assert p.parent == playerlist2

    def test_manual_list(self):
        """ This testcase creates two playerlists manually (means by explicit
         declaration of each PlayerList class & members) and moves one item
         from list 2 to list 1. As an element can have exactly one parent list
         this looks superweird, but is desired behaviour. In a real scenario
         one Player element would need to be deleted out of the list that it
         gets moved away from. To implement this seems overhead for me right
         now. """
        list1 :PlayerList = PlayerList(Table(), Player('Tester1'),Player('Tester2'))
        list2 :PlayerList = PlayerList(Table(), Player('Tester3'),Player('Tester4'))
        assert list1[0].parent == list1
        assert list1[1].parent == list1
        assert list2[0].parent == list2
        list1[0] = list2[0]
        assert list1[0].parent == list2[0].parent== list1 # weird, but correct 
        