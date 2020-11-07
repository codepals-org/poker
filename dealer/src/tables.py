""" The main function of this microservice - handle tables """

from fastapi import APIRouter, HTTPException, Response, Request, status
import mock_database as db

tables = APIRouter()

@tables.get('/', summary="Show tables")
async def show_tables():
    if db.phase == '':
        community_cards = []
    elif db.phase == 'flop':
        community_cards = db.community_cards[0:3]
    elif db.phase == 'turn':
        community_cards = db.community_cards[0:4]
    elif db.phase == 'river':
        community_cards = db.community_cards[0:5]
    return {"tables" : [{
        "table_id" : "1",
        "small_blind" : db.small_blind,
        "big_blind" : db.big_blind,
        "players" : [db.players],
        "community_cards" : community_cards
        }
    ]}

@tables.post('/1/next_round', summary="Next Round")
async def next_round():
    if db.phase == '':
        db.phase = 'flop'
    elif db.phase == 'flop':
        db.phase = 'turn'
    elif db.phase == 'turn':
        db.phase = 'river'
    elif db.phase == 'river':
        db.phase = '' # new round
    return {"round": db.phase}
