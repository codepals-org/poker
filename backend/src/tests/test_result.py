from dealer.helpers.result import results

pc = [ # player cards
    ("2H","5C"),
    ("5H","2C"),
    ("7H","8C"),
    ("8H","7C"),
    ("10H","KC"),
    ("2H","3C"),
]

cc = [ # community cards
    ("10H","JH","QH","KH","AH"), # royal flush
    ("9H","10H","JH","QH","KH"), # straight flush
    ("9H","9C","9S","9D","2C"),  # four of a kind
    ("9H","3H","4H","AH","KC"),  # flush
]

def test_result_algorithm_tests():
    # assert results(pc,cc[0]) == ((0, 1, 2, 3, 4, 5),
    #     ['Royal flush', 'Royal flush', 'Royal flush',
    #     'Royal flush', 'Royal flush', 'Royal flush'])
    assert results(pc,cc[1]) == ((0, 1, 2, 3, 4, 5),
        ['Straight flush', 'Straight flush', 'Straight flush',
        'Straight flush', 'Straight flush', 'Straight flush'])
    assert results(pc,cc[2]) == ((0, 1, 2, 3, 4, 5),
        ['Four of a kind', 'Four of a kind', 'Four of a kind',
        'Four of a kind', 'Four of a kind', 'Four of a kind'])
    assert results(pc,cc[3]) == ((4,), ['Flush'])