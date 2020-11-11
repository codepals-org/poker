import random

start_budget = 500
small_blind = 10
big_blind = 2 * small_blind
players = []
pot = 0
community_cards = []
phase = 0 # 0 = new round, 3 = flop, 4 = turn, 5 = river
game_started = False
round_started = False
round = 0

card_stack = [
    # Card Abbreviations: 
    # https://commons.wikimedia.org/wiki/Category:SVG_playing_cards
    "2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH", # hearts
    "2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD", # diamonds
    "2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS", # spade
    "2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC" # cross
]

random.shuffle(card_stack)

community_cards = (
    card_stack.pop(),
    card_stack.pop(),
    card_stack.pop(),
    card_stack.pop(),
    card_stack.pop()
    )