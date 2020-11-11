""" This module comes with functions to decide which poker player out 
of all players has the best cards. 
"""
import itertools
# full_list in [('A','A'),('B','B')...,('F','F')]

def results(full_list, public_card):
    """ The results function takes a list of player cards and 
    the community cards (in the middle of the table) and calculates
    who of the players has the wining hand. """

    #public_card =  ['6H', '6D', '5S', '4S', '8S']
    #full_list   =  [['9C', 'AS'], ['9H', '5C'], ['4D', '2S'], ['KC', '2D'], ['9D', '10C']]

    high_comb_rank  = []
    high_type_rank  = []
    high_point_rank = []
    public_card_temp = []
    winner_card_type = []
    public_card_temp.extend(list(public_card))
    total_players = len(full_list)

    for player_card_check in full_list:
        player_card_check += public_card
        card_combinations = list(itertools.combinations(player_card_check, 5))

        color_all = []
        size_all = []

        for card_combination in card_combinations:
            color_current = []
            for card in card_combination:
                color_current.append(str(card[-1]))
            color_all.append(color_current)

            size_current = []
            for card in card_combination:
                if card[-2].isdigit():
                    size5 = int(card[-2])
                    if size5 == 0:
                        size5 = 10
                else:
                    if card[-2] == "J":
                        size5 = 11
                    elif card[-2] == "Q":
                        size5 = 12
                    elif card[-2] == "K":
                        size5 = 13
                    elif card[-2] == "A":
                        size5 = 14
                size_current.append(size5)
            size_all.append(size_current)
        card_type_all = []
        type_score_all = []
        high_card_all = []
        win_point = []
        for i, card_combination in enumerate(card_combinations):
            print("Cards: " + str(card_combination) +", " + str(i))
            color = color_all[i]
            print("Color: " + str(color))
            size = size_all[i]
            print("Size: " + str(size))
            high_card = []
            card_type = []
            size_set = list(set(size))
            while len(set(color)) == 1:
                if max(size) - min(size) == 4:
                    card_type = 'Straight flush'
                    high_card = max(size)
                    break
                else:
                    card_type = 'Flush'
                    high_card = sum(size)
                    break
            else:
                if len(set(size)) == 5:
                    if max(size) - min(size) == 4:
                        if sorted(size)[2] == sum(size) / len(size):
                            card_type = 'Straight'
                            high_card = max(size)
                    elif max(size) - min(size) == 12:
                        if sum(size) == 28:
                            card_type = 'Straight'
                            high_card = 5
                        else:
                            card_type = 'High card'
                            high_card = sum(size)
                    else:
                        card_type = 'High card'
                        high_card = sum(size)

                elif len(size) - 1 == len(set(size)):
                    card_type = 'One pair'
                    high_card = max([x for n, x in enumerate(size) if x in size[:n]])

                elif len(size) - 2 == len(set(size)):
                    size_temp = []
                    size_temp.extend(size)
                    for a in range(0, 5):
                        for b in range(0, 3):
                            if size[a] == size_set[b]:
                                size[a] = 0
                                size_set[b] = 0
                    last = [x for x in size if x != 0]
                    size = []
                    size.extend(size_temp)
                    if last[0] == last[1]:
                        card_type = 'Three of a kind'
                        high_card = max([x for n, x in enumerate(size) if x in size[:n]])

                    else:
                        card_type = 'Two pairs'
                        high_card = sum([x for n, x in enumerate(size) if x in size[:n]])

                elif len(size) - 3 == len(set(size)):
                    for a in range(0, 5):
                        for b in range(0, 2):
                            if size[a] == size[b]:
                                size[a] = 0
                                size_set[b] = 0
                    last = [x for x in size if x != 0]

                    if last[0] == last[1] == last[2]:
                        card_type = 'Four of a kind'
                        high_card = max([x for n, x in enumerate(size) if x in size[:n]])

                    else:
                        card_type = 'Full house'
                        high_card = max([x for n, x in enumerate(size) if x in size[:n]])
            type_score = []
            if card_type == 'Straight flush':
                type_score = 9
            elif card_type == 'Four of a kind':
                type_score = 8
            elif card_type == 'Full house':
                type_score = 7
            elif card_type == 'Flush':
                type_score = 6
            elif card_type == 'Straight':
                type_score = 5
            elif card_type == 'Three of a kind':
                type_score = 4
            elif card_type == 'Two pairs':
                type_score = 3
            elif card_type == 'One pair':
                type_score = 2
            elif card_type == 'High card':
                type_score = 1
            card_type_all.append(card_type)
            high_card_all.append(high_card)
            win_point.append(type_score * int(100) + high_card)

        high_point = max(win_point)
        locate = win_point.index(max(win_point))
        high_comb = card_combinations[locate]
        high_type = card_type_all[locate]
        high_point_rank.append(high_point)
        high_comb_rank.append(high_comb)
        high_type_rank.append(high_type)
    winner = []
    for i in range(len(high_point_rank)):
        if high_point_rank[i] == max(high_point_rank):
            winner.extend(str(i))
    for i in winner:
        a = int(i)
        b = high_type_rank[a]
        winner_card_type.append(b)

    return (winner, winner_card_type)
