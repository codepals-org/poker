import random

small_blind = 10
big_blind = 2 * small_blind
players = dict()
pot = 0
community_cards = []
phase = '' # 'flop', 'turn', 'river'

card_stack = [
    # Card Abbreviations: 
    # https://commons.wikimedia.org/wiki/Category:SVG_playing_cards
    "2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH", # hearts
    "2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD", # diamonds
    "2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS", # spade
    "2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC" # cross
]

random.shuffle(card_stack)

players['player1'] = {
    "player_name" : "Player1",
    "player_secret" : "secret_1",
    "player_money_seat" : 500,
    "player_money_pot" : 0,
    "player_cards" : (card_stack.pop(), card_stack.pop()) 
}

players['player2'] = {
    "player_name" : "Player2",
    "player_secret" : "secret_2",
    "player_money_seat" : 500,
    "player_money_pot" : 0,
    "player_cards" : (card_stack.pop(), card_stack.pop())
}

players['player3'] = {
    "player_name" : "Player3",
    "player_secret" : "secret_3",
    "player_money_seat" : 500,
    "player_money_pot" : 0,
    "player_cards" : (card_stack.pop(), card_stack.pop())
}

community_cards = (
    card_stack.pop(),
    card_stack.pop(),
    card_stack.pop(),
    card_stack.pop(),
    card_stack.pop()
    )