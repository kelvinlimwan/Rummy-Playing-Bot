from valid_table import valid_table

def valid_move(card, to_group, table):
    '''Returns True if moving the `card` to the group in `table` with index
    `to_group` is valid, and False otherwise'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # sort `group` as per `card_values`
    group = table[to_group]
    group.sort(key=lambda x: values_dict[x[0]])

    # check if `group` is N-of-a-kind; if so, get required suits in group that
    # `card` could be and check if the card value is the same as all the cards
    # in `group` or if the card suit is correct; if not, `play` is not valid
    if group[0][0] == group[-1][0]:
        req_suits = ['S', 'H', 'C', 'D']
        for existing_card in group:
            if existing_card[1] in req_suits:
                req_suits.remove(existing_card[1])
        if not req_suits:
            req_suits = ['S', 'H', 'C', 'D']
        if card[0] == group[0][0] and card[1] in req_suits:
            return True
        else:
            return False

    # check if `group` is a run
    # get preceding value in the sequence that `card` could be
    first_index = card_values.index(group[0][0])
    if first_index == 0:
        preced_value = None
    else:
        preced_value = card_values[first_index - 1]
    # get next value in the sequence that `card` could be
    last_index = card_values.index(group[-1][0])
    if last_index == len(card_values) - 1:
        next_value = None
    else:
        next_value = card_values[last_index + 1]
    # get preceding suits in the sequence that `card` could be
    preced_suits = ['S', 'C']
    if group[0][1] in preced_suits:
        preced_suits = ['H', 'D']
    # get next suits in the sequence that `card` could be
    next_suits = ['S', 'C']
    if group[-1][1] in next_suits:
        next_suits = ['H', 'D']
    # check if card has both an adjacent value and alternating colour as the
    # first or last card in `group`; if not, `play` is not valid
    if ((card[0] != preced_value or card[1] not in preced_suits) and
            (card[0] != next_value or card[1] not in next_suits)):
        return False

    return True


def play_type1(play, hand, table):
    '''Returns True if the `play` is a valid play of type 1 given `hand` and
    `table`, and False otherwise'''

    card = play[2][0]
    to_group = play[2][1]

    # check if the card is in `hand` and if the group index is valid; if not,
    # `play` is not valid
    if card not in hand or to_group > len(table):
        return False

    # when the card is played in a group, use `valid_move` to determine if the
    # move is valid
    if to_group < len(table):
        return valid_move(card, to_group, table)

    return True


def play_type2(play, play_history, hand, table):
    '''Returns True if the `play` is a valid play of type 2 given
    `play_history`, `hand` and `table`, and False otherwise'''

    card = play[2][0]
    from_group = play[2][1]
    to_group = play[2][2]

    # check if the group indices are valid; if not, `play` is not valid
    if from_group >= len(table) or to_group > len(table):
        return False

    # check if the card is in the group in `table` with index `from_group` and
    # if it is not the first play of the turn; if not, `play` is not valid
    if card not in table[from_group] or play_history[-1][0] != play[0]:
        return False

    # when the card is played in a group, use `valid_move` to determine if the
    # move is valid
    if to_group < len(table):
        return valid_move(card, to_group, table)

    return True


def play_type3(play, play_history, hand, table):
    '''Returns True if the `play` is a valid play of type 3 given
    `play_history`, `hand` and `table`, and False otherwise'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # check if any play has been played by the player in this turn; if not,
    # `play` is not valid
    if not play_history or play_history[-1][0] != play[0]:
        return False

    # check if the table state is valid; if not, `play` is not valid
    if not valid_table(table):
        return False

    # check if it is an opening turn and create a corresponding boolean
    opening_turn = True
    for previous_play in play_history[::-1]:
        if previous_play[0] == play[0] and previous_play[1] == 3:
            opening_turn = False
            break

    # when it is an opening turn, check if the total of the points is at least
    # 24; if not, `play` is not valid
    if opening_turn:
        # create a list of values of cards played from the hand to the table in
        # opening turn
        cards_from_hand_list = []
        for previous_play in play_history[::-1]:
            if previous_play[0] == play[0] and previous_play[1] == 1:
                cards_from_hand_list.append(previous_play[2][0])
            elif previous_play[0] != play[0]:
                break
        # compute the total of the points using `values_dict`
        total = 0
        for card in cards_from_hand_list:
            total += values_dict[card[0]]
        # check if the total of the points is at least 24; if not, `play` is
        # not valid
        if total < 24:
            return False

    return True


def valid_play(play, play_history, active_player, hand, table):
    '''Returns True if the `play` is valid given `play_history`- the
    combination of the plays made to date, `active_player`- the player whose
    turn it is to play, `hand`- the content of the player's hand and `table`-
    the groups on the table, and False otherwise'''

    # check if the player attempting to play is the `active_player`; if not,
    # `play` is not valid
    if play[0] != active_player:
        return False

    # when the player picks a card, `play` is valid
    if play[1] == 0:
        return True

    # when type of `play` is 1, 2 or 3, use `play_type1`, `play_type2` and
    # `play_type3` respectively to determine if `play` is valid
    elif play[1] == 1:
        return play_type1(play, hand, table)
    elif play[1] == 2:
        return play_type2(play, play_history, hand, table)
    else:
        return play_type3(play, play_history, hand, table)

