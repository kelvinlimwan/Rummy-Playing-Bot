def score(cards):
    '''Returns the score for `cards`- the list of cards held by the player'''

    # create a dictionary to assign a number to each card value
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # compute the score of `cards`
    score = 0
    for card in cards:
        score += values_dict[card[0]]

    return score
