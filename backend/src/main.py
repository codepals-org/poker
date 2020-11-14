""" Contains all the things required to run the FASTAPI """

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dealer.api.tables import tables
from dealer.api.players import players

import sys
sys.path.insert(1, '.')

app = FastAPI()

# CORS middleware allows other clients (with different host/ip/port)
# to consume the REST-API

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(request: Request):
    return {
        "welcome_message":  "Welcome to the Poker Server. I'm your dealer."
            + " Visit /docs to find out about how to use me to"
            + " serve the poker game.",
        "docs_url": "http://" + request.client.host + ":" + str(request.url.port) + "/docs"}

app.include_router(tables, prefix='/api/v1/tables', tags=['tables'])
app.include_router(players, prefix='/api/v1/players', tags=['players'])
