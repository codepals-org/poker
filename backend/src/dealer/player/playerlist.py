from .player import Player, Role
from typing import List
import logging

class PlayerList(list):
    def __init__(self):
        super()

    def active_player(self) -> Player:
        for player in self:
            if player.active == True:
                return player
        return None

    def circular_button_move(self) -> None:
        """ moves the each role to the player sitting on the left in case we 
        have two players it will remove the dealer role """
        last_role = self[-1].role
        for position, player in reversed(list(enumerate(self))):
            logging.debug("position: %s role: %s", position, player.role)
            if position == 0:
                player.role = last_role
            else:
                player.role = self[position-1].role
        for position, player in enumerate(self):
            logging.debug("position: %s role: %s", position, player.role)

    def handout_cards(self, cardstack :list) -> None:
        for player in self:
            player.hand.append(cardstack.pop())
        for player in self:
            player.hand.append(cardstack.pop())

    def init_buttons(self) -> None:
        """ In the beginning of the game there are no buttons on each players seat.
        This function gives each player a button-role instead. """
        count = len(self)
        if count <2:
            raise ValueError("At least two players needed.")
        elif count == 2:
            self[0].role = Role.SMALL
            self[1].role = Role.BIG
        elif count > 2:
            self[0].role = Role.DEALER
            self[1].role = Role.SMALL
            self[2].role = Role.BIG
            if count > 3:
                self[3].role = Role.UTG

    def deduct_blinds(self, big_blind :float, small_blind :float):
        for player in self:
            if player.role == Role.BIG:
                if player.money_seat < big_blind:
                    player.money_pot = player.money_seat
                    player.money_seat = 0.0
                else:
                    player.money_seat -= big_blind
                    player.money_pot += big_blind
            if player.role == Role.SMALL:
                if player.money_seat < small_blind:
                    player.money_pot = player.money_seat
                    player.money_seat = 0.0
                else:
                    player.money_seat -= small_blind
                    player.money_pot += small_blind

    def who_starts(self) -> Player:
        """ Who will start with betting """
        if len(self) > 3:
            starter_role = Role.UTG
        elif len(self) == 3:
            starter_role = Role.DEALER
        elif len(self) == 2:
            starter_role = Role.SMALL
        else:
            raise RuntimeError(
                "It seems like there is not enough players to start")
        for p in self:
            if p.role == starter_role:
                return p