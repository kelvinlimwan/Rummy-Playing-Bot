def n_of_a_kind(group):
    '''Returns True if the `group` is a valid N-of-a-kind, and False
    otherwise'''

    # check if there are less than 3 cards `group`; if so, `group` is not a
    # valid N-of-a-kind
    if len(group) < 3:
        return False

    # check if all cards in `group` have the same value; if not, `group` is not
    # a valid N-of-a-kind
    value = group[0][0]  # initial value of first card
    for card in group[1:]:
        if card[0] != value:
            return False

    suits_in_group = []
    # when there are exactly 3 cards in `group`, check if each card has a
    # unique suit; if not, `group` is not a valid N-of-a-kind
    if len(group) == 3:
        for card in group:
            if card[1] in suits_in_group:
                return False
            else:
                suits_in_group.append(card[1])
        return True
    # when there are more than 3 cards in `group`, check if all suits are
    # present; if not, `group` is not a valid N-of-a-kind
    else:
        for card in group:
            if card[1] not in suits_in_group:
                suits_in_group.append(card[1])
                if len(suits_in_group) == 4:
                    return True
        return False

def run(group):
    '''Returns True if the `group` is a valid run, and False otherwise'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # check if there are less than 3 cards `group`; if so, `group` is not a
    # valid run
    if len(group) < 3:
        return False

    # sort `group` as per `card_values`
    group.sort(key=lambda x: values_dict[x[0]])

    # check if `group` is a continuous sequence in terms of value and
    # alternating in colour; if not, `group` is not a valid run
    preced_card_value = group[0][0]  # initial value of first card
    preced_card_suit = group[0][1]  # initial suit of first card
    for card in group[1:]:
        # get `next_value` that `card` should be
        preced_index = card_values.index(preced_card_value)
        if preced_index == len(card_values) - 1:
            next_value = None
        else:
            next_value = card_values[preced_index + 1]
        # get `suits` that `card` should be
        next_suits = ['S', 'C']
        if preced_card_suit in next_suits:
            next_suits = ['H', 'D']
        # check if `card` has a value higher than one and alternating in colour
        # as compared to the previous card
        if card[0] != next_value or card[1] not in next_suits:
            return False
        # set `card` as preceding card, for looping
        preced_card_value = card[0]
        preced_card_suit = card[1]

    return True

def valid_table(groups):
    '''Returns True if all `groups` are valid N-of-a-kinds or runs, and False
    otherwise'''

    # for each `group`, check if it is a valid N-of-a-kind or a valid run; if
    # not, `groups` is not valid
    for group in groups:
        if not (n_of_a_kind(group) or run(group)):
            return False

    return True
