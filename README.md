# Pokerproject - Poker Server & Clients

We build a Poker Game consisting of a Pokerserver ("Dealer") and multiple Clients ("Players"). 

**How to contribute:** 

1) Join our Codepals events. 
2) Check the issues list and see where you can help
3) Create new features for the PokerServer (and implement them after discussion)

## Scope 
What should the Server/Dealer be able to do?

- [X] shuffling cards
- [X] handing out chips
- [ ] keeping track of them
- [X] dealers sets the blinds
- [X] knows all the cards
- [ ] he makes the result
- [ ] keep track of overall performance by storing the money to a database
- [ ] who's turn is it?
- [ ] split pot

What should the Client/Player be able to do?

- [ ] ask the dealer: how much chips do I have left?
- [ ] ask the dealer: how much chips do the others have?
- [ ] say "I'm ready"
- [ ] call
- [ ] bet / raise
- [ ] fold
- [ ] if I lose, I don't want to show my cards

## Installation

### Clone this repository

Run this in your commandline (requires git on your computer)

```git clone https://github.com/codepals-org/poker.git```

### Install & Run -- Backend / Dealer / Server

Requirements: Python 3 must be installed on your computer (for backend/dealer/server), you need a connection to the internet

1. ```cd poker\backend``` -- go to the backend folder
2. ```python3 -m venv .venv``` -- create a virtual environment for python
3. ```source ./.venv/bin/activate``` (Mac/Linux) or ```./.venv/Scripts/activate.ps1``` (Windows) -- activate the virtual environment
    
    If you are using Windows, you may get an authorization issue in Powershell, please then execute the following command ```sourceSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser``` (further details can be found in [Windows Docs](https://docs.microsoft.com/de-de/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7))

4. ```pip install --upgrade pip``` & ```pip install -r requirements.txt``` -- install latest packages needed to run the server
5. ```cd src``` -- change to the sourcecodes directory 
6. ```uvicorn main:app --reload``` -- run a simple webserver, which will update on changes 
7. open [http://localhost:8000](http://localhost:8000) in your webbrowser --> You should see a Welcome Page.
8. open [http://localhost:8000/docs](http://localhost:8000/docs) in your webbrowser --> You will find a Swagger documentation of the REST-API. 

For further instructions & support visit our Codepals Meetup in Beijing online or offline :)

### Install & Run -- Player / Client

Whereas there is exactly one Server hosting the game, there are multiple Clients that have their own character, algorithms. Just like in reallife.
It is up to each developer to program it's own Poker Player. Therefore there is no official guideline how to install. Each developer is asked to 
provide a installation instruction for his client in order to simulate Poker games. 
