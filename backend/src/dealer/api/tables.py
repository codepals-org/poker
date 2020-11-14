""" The main function of this endpoint - handle tables """

from fastapi import APIRouter, HTTPException, Response, Request, status
import dealer.helpers.mock_database as db
from dealer.helpers.result import results
from pydantic import BaseModel
from typing import Optional, List, Tuple
import random

tables = APIRouter()

@tables.get('/', summary="Show tables")
async def show_tables():
    if db.phase == 0:
        community_cards = []
    else:
        community_cards = db.community_cards[0:db.phase]
    return {"tables" : [{
        "table_id" : "0",
        "small_blind" : db.small_blind,
        "big_blind" : db.big_blind,
        "game_started" : db.game_started,
        "round_started" : db.round_started,
        "players" : db.players,
        "community_cards" : community_cards
        }
    ]}

@tables.get('/0', 
    summary="Show the one and only table (maybe in future multiple tables)")
async def show_one_table():
    if db.phase == 0:
        community_cards = []
    else:
        community_cards = db.community_cards[0:db.phase]
    return {
        "table_id" : "0",
        "small_blind" : db.small_blind,
        "big_blind" : db.big_blind,
        "game_started" : db.game_started,
        "round_started" : db.round_started,
        "players" : db.players,
        "community_cards" : community_cards
        }

@tables.get('/0/results')
async def who_wins():
    if db.phase != 5:
        raise HTTPException(status_code=403, detail="Too early.")
    else:
        player_cards = []
        for player in db.players:
            player_cards.append(player.get('player_cards'))
        return {"result": results(player_cards, db.community_cards)}

@tables.post('/0/start_game', summary="Start the game. Lock players from signup.",
            status_code=200)
async def start_game():
    if start_game():
        db.game_started = True
        return {"message": "Game started."}
    else:
        raise HTTPException(status_code=403,
            detail="Game already started or not enough players.")

@tables.post('/0/next_round', summary="Next Round")
async def next_round():
    if db.phase == 0:
        db.phase += 3
    elif db.phase == 5:
        db.phase = 0 # new round
    else:
        db.phase += 1 
    return {"round": db.phase}

def start_game() -> bool:
    if db.round == 0 and len(db.players) >= 2:
        db.game_started = True
        db.round_started = True
        print("Number of players: " + str(len(db.players)))
        random_player = random.randint(0, len(db.players)-1)
        print("Random result: " + str(random_player))
        sb_player = db.players[random_player]
        if random_player == len(db.players)-1:
            # random player / small blind is the last player in the list
            bb_player = db.players[0] # start from left
            next_player = db.players[1]
        else:
            bb_player = db.players[random_player+1]
            if random_player+2 == len(db.players)-1:
            # big blind is the last plaser in the list
                next_player = db.players[0] # start from left
            else:
                next_player = db.players[random_player+2]
        sb_player['player_role'] = 'small_blind'
        sb_player['player_money_pot'] += db.small_blind
        sb_player['player_money_seat'] -= db.small_blind 
        bb_player['player_role'] = 'big_blind'
        bb_player['player_money_pot'] += db.big_blind
        bb_player['player_money_seat'] -= db.big_blind
        next_player['player_active'] = True
        db.round = 1
        return True # Game started
    else:
        return False # Game already started before or not enough players


