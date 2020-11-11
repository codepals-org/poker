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
    player_name : str
    secret: str

class PlayerSignUp(BaseModel):
    """ For registration of a new player we need just a player name.
    The dealer will take care of the budget, etc. """
    player_name : str

class Player(BaseModel):
    """ The full player attributes, without his cards
    and without the secret """
    player_name :str
    player_name :str
    player_money_seat :float
    player_money_pot :float
    player_role :str
    player_active :bool

class PlayerFull(BaseModel):
    """ The full player attributes, without his cards 
    but with his secret in order to authorize further 
    interactions with the game """
    player_name :str
    player_name :str
    player_money_seat :float
    player_money_pot :float
    player_role :str
    player_active :bool
    payler_secret : str

@players.get('/', summary="Show players")
async def show_players():
    return [db.players]

@players.get('/{player_id}',
    summary="Show single player",
    status_code=200,
    response_model=Player)
async def get_player_profile(player_id : str):
    return db.players[player_id]

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

@players.put('/{player_id}', response_model=Player, summary="Update player name", status_code=200)
async def update_player(player_id: int, player: PlayerSignUp):
    db.players[player_id]['player_name']=player.player_name
    return db.players[player_id]

@players.post('/', response_model=Player)
async def signup_new_player(player :PlayerSignUp):
    if db.game_started == True:
        raise HTTPException(status_code=403, detail="Game has started.")
    else:
        new_id = len(db.players)
        db.players.append(
            {
                "player_id": new_id,
                "player_name": player.player_name,
                "player_money_seat": db.start_budget,
                "player_money_pot": 0,
                "player_role": 'normal',
                "player_active": False
            }
        )
        return db.players[new_id]

@players.post('/{player_id}/call')
async def callpot(player_id : str, secret :Secret):
    if secret.secret != db.players[player_id].get('player_secret'):
        pass
    return {"message": "call"}

@players.post('/{player_id}/raise')
async def raisepot(player_id : str, secret :Secret):
    if secret.secret != db.players[player_id].get('player_secret'):
        pass
    return {"message": "raise"}

@players.post('/{player_id}/fold')
async def fold(player_id : str, secret :Secret):
    if secret.secret != db.players[player_id].get('player_secret'):
        pass
    return {"message": "fold"}
