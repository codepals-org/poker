""" The main function of this endpoint - handle players & client functions """

from fastapi import APIRouter, HTTPException, Response, Request, status, Body
from fastapi.responses import JSONResponse
import mock_database as db
import json
from pydantic import BaseModel
from typing import Optional, List

players = APIRouter()

class Secret(BaseModel):
    """ Each player has a secret. If it gets passed in the post request,
     we assume the player itself or his poker bot is doing that to see 
     his own cards """
    secret: str = None

@players.get('/', summary="Show players")
async def show_players():
    return [db.players]

@players.post('/{player_id}', summary="Show single player", status_code=200)
async def show_player(player_id : str, secret :Secret):
    answer = {
            "player_id" : db.players[player_id].get('player_id'),
            "player_name" : db.players[player_id].get('player_name'),
            "player_money_seat" : db.players[player_id].get('player_money_seat'),
            "player_money_pot" : db.players[player_id].get('player_money_pot'),
            "player_role": db.players[player_id].get('player_role'),
            "player_active" : db.players[player_id].get('player_active')
        }
    if secret.secret != db.players[player_id].get('player_secret'):
            return JSONResponse(content=answer, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        # if authorized add the two secret cards to the response
        answer.update({"player_cards" : db.players[player_id].get('player_cards')})
    return JSONResponse(content=answer)

# @players.post('/{player_id}/call')
# async def call(player_id :str, res):
#     return 
