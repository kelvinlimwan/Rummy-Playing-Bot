full_turn = []  # global variable

def n_of_a_kind(group):
    '''Returns True if the `group` is a valid N-of-a-kind, and False
    otherwise'''

    # `group` is not a valid N-of-a-kind if there are less than 3 cards in it
    if len(group) < 3:
        return False

    # when a joker is in `group`
    if 'XX' in group:
        # remove the joker from a `group` copy
        group_without_joker = group.copy()
        group_without_joker.remove('XX')

        # `group` is not a valid N-of-a-kind if not all the cards have the same
        # value, excluding jokers
        value = group_without_joker[0][0]
        for card in group_without_joker[1:]:
            if card[0] != value:
                return False

        suits_in_group = []
        # `group` is not a valid N-of-a-kind if there are two or three cards
        # and they do not all have different suits
        if len(group_without_joker) <= 3:
            for card in group_without_joker:
                if card[1] in suits_in_group:
                    return False
                else:
                    suits_in_group.append(card[1])
            return True

        # `group` is a valid N-of-a-kind if there are more than three cards and
        # there is at least three suits present
        else:
            for card in group_without_joker:
                if card[1] not in suits_in_group:
                    suits_in_group.append(card[1])
                    if len(suits_in_group) == 3:
                        return True
            return False

    # when there is no joker in `group`
    else:
        # `group` is not a valid N-of-a-kind if not all the cards have the same
        # value, excluding jokers
        value = group[0][0]
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

    # `group` is not a valid N-of-a-kind if there are less than 3 cards in it
    if len(group) < 3:
        return False

    # when a joker is in `group`
    if 'XX' in group:
        # remove the joker from a copy of `group` and sort it as per
        # `card_values`
        group_without_joker = group.copy()
        group_without_joker.remove('XX')
        group_without_joker.sort(key=lambda x: values_dict[x[0]])

        # check if run is a continuous sequence in terms of value without
        # joker; it there are more than 1 'hole' in the sequence, run is not
        # valid
        continuous = True
        orig_index = card_values.index(group_without_joker[0][0])
        card_index = 0
        number_of_missing_cards = 0
        insert_index = 0
        adj_suit = ''
        for card in group_without_joker[1:]:
            new_index = card_values.index(card[0])
            if new_index == orig_index + 1:
                orig_index = new_index
            else:
                continuous = False
                number_of_missing_cards += 1
                insert_index = group_without_joker.index(card)
                adj_suit = card[1]
                if number_of_missing_cards == 1:
                    card_index = new_index
                elif number_of_missing_cards > 1:
                    return False

        # when run is not a continuous sequence in terms of value without joker
        if not continuous:
            missing_value = card_values[card_index - 1]
            pot_suits = ['S', 'C']
            if adj_suit in pot_suits:
                pot_suits = ['H', 'D']
            joker = missing_value + pot_suits[0]
            group_without_joker.insert(insert_index, joker)

        # check if run is alternating in colour; if not, `group` is not a valid
        # run
        preced_card_suit = group_without_joker[0][1]
        for card in group_without_joker[1:]:
            next_suits = ['S', 'C']
            if preced_card_suit in next_suits:
                next_suits = 'HD'
            if card[1] not in next_suits:
                return False
            preced_card_suit = card[1]

    # when there is no joker in `group`
    else:
        # sort `group` as per `card_values`
        group.sort(key=lambda x: values_dict[x[0]])

        # check if `group` is a continuous sequence in terms of value and
        # alternating in colour; if not, `group` is not a valid run
        preced_card_value = group[0][0]
        preced_card_suit = group[0][1]
        for card in group[1:]:
            preced_index = card_values.index(preced_card_value)
            if preced_index == len(card_values) - 1:
                next_value = None
            else:
                next_value = card_values[preced_index + 1]
            next_suits = ['S', 'C']
            if preced_card_suit in next_suits:
                next_suits = ['H', 'D']
            if card[0] != next_value or card[1] not in next_suits:
                return False
            preced_card_value = card[0]
            preced_card_suit = card[1]

    return True


def joker_replace(group):
    '''Returns a list of cards that the joker is potentially replacing in a
    valid `group`'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # remove the joker from a copy of `group` and sort it as per `card_values`
    group_without_joker = group.copy()
    group_without_joker.remove('XX')
    group_without_joker.sort(key=lambda x: values_dict[x[0]])

    # when group is N-of-a-kind
    if group_without_joker[0][0] == group_without_joker[-1][0]:
        # get potential suits that joker could take
        pot_suits = ['S', 'H', 'C', 'D']
        for card in group:
            if card[1] in pot_suits:
                pot_suits.remove(card[1])
        # if all suits are present, joker can take any suits
        if not pot_suits:
            pot_suits = ['S', 'H', 'C', 'D']
        # list of cards that joker can take
        return_list = [group_without_joker[0][0] + suit for suit in pot_suits]

    # when group is run
    else:
        # check if run is a continuous sequence without joker
        continuous = True
        card_index = card_values.index(group_without_joker[0][0])
        adj_suit = ''
        for card in group_without_joker[1:]:
            new_index = card_values.index(card[0])
            if new_index == card_index + 1:
                card_index = new_index
            else:
                adj_suit = card[1]
                continuous = False
                break

        # when run is a continuous sequence without joker
        if continuous:
            # when run starts with 'A'
            if group_without_joker[0][0] == 'A':
                pot_suits = ['S', 'C']
                if group_without_joker[-1][1] in pot_suits:
                    pot_suits = ['H', 'D']
                return_list = []
                last_index = card_values.index(group_without_joker[-1][0])
                next_value = card_values[last_index + 1]
                return_list = [next_value + suit for suit in pot_suits]
            # when run ends with 'K'
            elif group_without_joker[-1][0] == 'K':
                pot_suits = ['S', 'C']
                if group_without_joker[0][1] in pot_suits:
                    pot_suits = ['H', 'D']
                return_list = []
                first_index = card_values.index(group_without_joker[0][0])
                preced_value = card_values[first_index - 1]
                return_list = [preced_value + suit for suit in pot_suits]
            # when group does not contain 'A' or 'K'
            else:
                first_index = card_values.index(group_without_joker[0][0])
                preced_value = card_values[first_index - 1]
                preced_suits = ['S', 'C']
                if group_without_joker[0][1] in preced_suits:
                    preced_suits = ['H', 'D']
                preced_list = [preced_value + suit for suit in preced_suits]
                last_index = card_values.index(group_without_joker[-1][0])
                next_value = card_values[last_index + 1]
                next_suits = ['S', 'C']
                if group_without_joker[-1][1] in next_suits:
                    next_suits = ['H', 'D']
                next_list = [next_value + suit for suit in next_suits]
                return_list = preced_list + next_list

        # when run is not a continuous sequence without joker
        else:
            missing_value = card_values[card_index + 1]
            pot_suits = ['S', 'C']
            if adj_suit in pot_suits:
                pot_suits = ['H', 'D']
            return_list = [missing_value + suit for suit in pot_suits]

    return return_list


def create_groups_list(real_hand, jokers=[]):
    '''Returns a list of all possible N-of-a-kind groups and run groups that
    can be created from `real_hand`- the content of the player's hand excluding
    the joker and `jokers`- the list of jokers in the player's hand, sorted in
    descending order of group sizes'''

    card_values = 'A234567890JQK'

    # when `hand` contains only jokers
    if not real_hand:
        return []

    groups_list = []
    # add N-of-a-kind groups
    group = [real_hand[0]]
    mod_real_hand = real_hand + ['ZZ']
    for card in mod_real_hand[1:]:
        if card[0] == group[0][0] and len(group) <= 3:
            diff_suit = True
            for prev_card in group:
                if prev_card[1] == card[1]:
                    diff_suit = False
                    break
            if diff_suit:
                group.append(card)
        elif card[0] == group[0][0] and len(group) > 3:
            group.append(card)
        else:
            if len(group) < 3 and jokers:
                group.append('XX')
            if len(group) >= 3:
                groups_list.append(group)
            group = [card]

    # add run groups
    real_hand_copy = real_hand.copy()
    for anchor_card in real_hand:
        if anchor_card in real_hand_copy:
            group = [anchor_card]
            real_hand_copy.remove(anchor_card)
            for card in real_hand_copy:
                first_index = card_values.index(group[-1][0])
                if first_index == 0:
                    preced_value = None
                else:
                    preced_value = card_values[first_index - 1]
                preced_suits = ['S', 'C']
                if group[-1][1] in preced_suits:
                    preced_suits = ['H', 'D']
                if preced_value and card in [preced_value + preced_suits[0],
                                             preced_value + preced_suits[1]]:
                    group.append(card)
                elif card_values.index(card[0]) < first_index - 1:
                    break
            if len(group) < 3 and jokers:
                group.append('XX')
            if len(group) >= 3:
                for card in group[1:]:
                    if card != 'XX':
                        real_hand_copy.remove(card)
                groups_list.append(group)

    return sorted(groups_list, key=len, reverse=True)


def valid_move(card, to_group, table):
    '''Returns True if moving the `card` to the group in `table` with index
    `to_group` is valid, and False otherwise'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    group = table[to_group]
    # when a joker is in `group`
    if 'XX' in group:
        # it is not allowed to have two jokers in a group
        if card == 'XX':
            return False

        pot_cards = joker_replace(group)
        for option in pot_cards:
            # remove the joker from a copy of `group` and sort it as per
            # `card_values`
            new_group = group.copy() + [option]
            new_group.remove('XX')
            new_group.sort(key=lambda x: values_dict[x[0]])

            # when `new_group` is N-of-a-kind, check if the addition of `card`
            # makes it a valid N-of-a-kind
            if new_group[0][0] == new_group[-1][0]:
                req_suits = ['S', 'H', 'C', 'D']
                for existing_card in new_group:
                    if existing_card[1] in req_suits:
                        req_suits.remove(existing_card[1])
                if not req_suits:
                    req_suits = ['S', 'H', 'C', 'D']
                if card[0] == new_group[0][0] and card[1] in req_suits:
                    return True

            # when `new_group` is a run, check if the addition of `card` makes
            # it a valid run
            else:
                first_index = card_values.index(new_group[0][0])
                if first_index == 0:
                    preced_value = None
                else:
                    preced_value = card_values[first_index - 1]
                last_index = card_values.index(new_group[-1][0])
                if last_index == len(card_values) - 1:
                    next_value = None
                else:
                    next_value = card_values[last_index + 1]
                preced_suits = ['S', 'C']
                if new_group[0][1] in preced_suits:
                    preced_suits = ['H', 'D']
                next_suits = ['S', 'C']
                if new_group[-1][1] in next_suits:
                    next_suits = ['H', 'D']
                # play is valid if card has both an adjacent value and
                # alternating colour as the first or last card in `new_group`
                if ((card[0] == preced_value and card[1] in preced_suits) or
                        (card[0] == next_value and card[1] in next_suits)):
                    return True

        return False

    # when there is no joker in `group`
    else:
        # when `card` is a joker and `group` is not 8-of-a-kind, play is valid
        if card == 'XX':
            if ((n_of_a_kind(group) and len(group) == 8) or
                    (run(group) and len(group) == 13)):
                return False
            return True

        # sort `group` as per `card_values`
        group.sort(key=lambda x: values_dict[x[0]])

        # when `group` is N-of-a-kind, check if the addition of `card` makes it
        # a valid N-of-a-kind
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

        # when `group` is a run, check if the addition of `card` makes it a
        # valid run
        first_index = card_values.index(group[0][0])
        if first_index == 0:
            preced_value = None
        else:
            preced_value = card_values[first_index - 1]
        last_index = card_values.index(group[-1][0])
        if last_index == len(card_values) - 1:
            next_value = None
        else:
            next_value = card_values[last_index + 1]
        preced_suits = ['S', 'C']
        if group[0][1] in preced_suits:
            preced_suits = ['H', 'D']
        next_suits = ['S', 'C']
        if group[-1][1] in next_suits:
            next_suits = ['H', 'D']
        # play is valid if card has both an adjacent value and alternating
        # colour as the first or last card in `group`
        if ((card[0] == preced_value and card[1] in preced_suits) or
                (card[0] == next_value and card[1] in next_suits)):
            return True

        return False


def move_one_place_one(active_player, real_hand, table):
    '''Returns a list of two valid moves for `active_player` to move a card
    from a group on the `table` to another and then place a card from
    `real_hand`- the content of the player's hand excluding the joker, in
    a group, a list of groups in the new table and a list of card in the new
    hand'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    new_moves = []
    new_table = []
    new_real_hand = []
    for anchor_group in table:
        from_group = table.index(anchor_group)
        # when `anchor_group` is N-of-a-kind
        if n_of_a_kind(anchor_group):
            iterator = set(anchor_group)
        # when `anchor_group` is a run and contains a joker
        elif 'XX' in anchor_group:
            anchor_group_copy = anchor_group.copy()
            anchor_group_copy.remove('XX')
            anchor_group_copy.sort(key=lambda x: values_dict[x[0]])
            iterator = [anchor_group_copy[0], anchor_group_copy[-1], 'XX']
        # when `anchor_group` is a run and does not contain a joker
        else:
            anchor_group.sort(key=lambda x: values_dict[x[0]])
            iterator = [anchor_group[0], anchor_group[-1]]
        table_copy = table.copy()
        table_copy.remove(anchor_group)
        # for each movable card in `anchor_group`
        for move_card in iterator:
            # for each destination group
            for dest_group in table_copy:
                to_group = table.index(dest_group)
                # check if `move_card` can be moved to the destination group;
                # if so, update a copy of the table state
                if valid_move(move_card, to_group, table):
                    table_copy2 = [[card for card in group] for group in table]
                    table_copy2[from_group].remove(move_card)
                    table_copy2[to_group] += [move_card]
                    # for each card in the hand excluding jokers
                    for place_card in real_hand:
                        # check if `place_card` can be moved to the
                        # `anchor_group`; if so, update `new_moves`,
                        # `new_table` and `new_real_hand`
                        if ((move_card == 'XX' and
                             place_card in joker_replace(anchor_group)) or
                                (move_card != 'XX' and
                                 valid_move(place_card, from_group, table_copy2))):
                            play1 = (active_player, 2, (move_card, from_group,
                                                        to_group))
                            play2 = (active_player, 1, (place_card,
                                                        from_group))
                            new_moves = [play1, play2]
                            new_table = table_copy2
                            new_table[from_group] += [place_card]
                            new_real_hand = real_hand.copy()
                            new_real_hand.remove(place_card)
                            return new_moves, new_real_hand, new_table
                        # check if `place_card` can be moved to the
                        # `dest_group`; if so, update `new_moves`,
                        # `new_table` and `new_real_hand`
                        elif (valid_move(place_card, to_group, table_copy2) and
                              (n_of_a_kind(table_copy2[from_group]) or
                               run(table_copy2[from_group]))):
                            play1 = (active_player, 2, (move_card, from_group,
                                                        to_group))
                            play2 = (active_player, 1, (place_card, to_group))
                            new_moves = [play1, play2]
                            new_table = table_copy2
                            new_table[to_group] += [place_card]
                            new_real_hand = real_hand.copy()
                            new_real_hand.remove(place_card)
                            return new_moves, new_real_hand, new_table

    return new_moves, new_real_hand, new_table


def opening_function(active_player, real_hand, table):
    '''Returns True and creates a list of plays in `opening_turn_full` when the
    opening turn can be played given `active_player`, `real_hand`- the content
    of the player's hand excluding jokers and `table`, and False otherwise'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # use global variable
    global full_turn

    # compute the total points of the six highest cards in `real_hand` and
    # check if it is less than 24; if so, pick a card
    max_opening_points = 0
    for card in real_hand[:6]:
        max_opening_points += values_dict[card[0]]
    if max_opening_points < 24:
        return False

    # list of all possible N-of-a-kind groups and run groups that can be
    # created from `real_hand`
    groups_list = create_groups_list(real_hand)

    # list of 2-tuples with each group and their points and sorted in
    # descending order of points
    points_list = []
    for group in groups_list:
        points = 0
        for card in group:
            points += values_dict[card[0]]
        points_list.append((group, points))
    points_list.sort(key=lambda x: x[1], reverse=True)

    # check if it is possible to play 2 groups of 3 from `real_hand` and if the
    # combined points is at least 24
    number_of_cards = 0
    points_of_groups = 0
    two_groups_of_three = []
    for group, points in points_list:
        if number_of_cards == 6:
            break
        # check if no card is repeating from first group
        no_rep = True
        if two_groups_of_three:
            for card in two_groups_of_three[0]:
                count = (two_groups_of_three[0].count(card) +
                         group.count(card))
                if card in group and count > real_hand.count(card):
                    no_rep = False
        if len(group) == 3 and no_rep:
            if number_of_cards == 0:
                number_of_cards += 3
                points_of_groups += points
                two_groups_of_three.append(group)
            elif number_of_cards == 3:
                points_of_groups += points
                if points_of_groups >= 24:
                    number_of_cards += 3
                    two_groups_of_three.append(group)
                break
    # when it is possible, create a list of plays in `full_turn`
    if number_of_cards == 6:
        to_group = len(table)
        for group in two_groups_of_three:
            for card in group:
                play = (active_player, 1, (card, to_group))
                full_turn.append(play)
            to_group += 1
        return True

    # check if it is possible to play 1 group of N from `real_hand`
    points_of_play = 0
    first_moves = []
    remaining_cards = real_hand.copy()
    table_copy = [[card for card in group] for group in table]
    to_group = len(table)
    for n in range(6, 2, -1):
        for group, points in points_list:
            if len(group) == n:
                points_of_play = points
                table_copy.append([])
                for card in group:
                    play = (active_player, 1, (card, to_group))
                    first_moves.append(play)
                    table_copy[to_group] += [card]
                    remaining_cards.remove(card)
                break
        if first_moves:
            break

    # add the remaining cards to existing groups on `table
    second_moves = []
    rem = 6 - len(first_moves)
    restart = True
    while restart:
        restart = False
        for card in remaining_cards.copy():
            if rem == 0:
                break
            for to_group in range(len(table_copy)):
                if valid_move(card, to_group, table_copy):
                    points_of_play += values_dict[card[0]]
                    play = (active_player, 1, (card, to_group))
                    second_moves.append(play)
                    table_copy[to_group] += [card]
                    remaining_cards.remove(card)
                    rem -= 1
                    restart = True
                    break

    # move groups on `table` to add the last remaining cards
    third_moves = []
    first_hand = remaining_cards
    first_table = table_copy
    for i in range(1, rem // 2):
        new_moves, new_hand, new_table = move_one_place_one(active_player,
                                                            first_hand,
                                                            first_table)
        third_moves += new_moves
        first_hand = new_hand
        first_table = new_table
        if not new_hand:
            break
    # add points of remaining cards to play to `points_of_play`
    for play in third_moves:
        if play[1] == 1:
            card = play[2][0]
            points_of_play += values_dict[card[0]]

    # when the combined points is at least 24 and plays are possible, create a
    # list of plays in `full_turn`
    if points_of_play >= 24 and (first_moves or second_moves or third_moves):
        full_turn = first_moves + second_moves + third_moves
        if third_moves and full_turn == third_moves:
            full_turn[0], full_turn[1] = full_turn[1], full_turn[0]
        return True

    return False


def normal_function(active_player, real_hand, jokers, table):
    '''Returns True and creates a list of plays in `normal_turn_full` when a
    normal turn can be played given `active_player`, `real_hand`- the content
    of the player's hand excluding jokers, `jokers`- the list of jokers in the
    player's hand and `table`, and False otherwise'''

    # use global variable
    global full_turn

    # list of all possible N-of-a-kind groups and run groups that can be
    # created from `hand`
    groups_list = create_groups_list(real_hand, jokers)

    # check if it is possible to play 2 groups of 3 from `hand`
    number_of_cards = 0
    two_groups_of_three = []
    for group in groups_list[::-1]:
        if number_of_cards == 6:
            break
        # check if no card is repeating from first group
        no_rep = True
        if two_groups_of_three:
            for card in two_groups_of_three[0]:
                count = (two_groups_of_three[0].count(card) +
                         group.count(card))
                if (card == 'XX' and card in group and
                        count > jokers.count(card)):
                    no_rep = False
                elif (card != 'XX' and card in group and
                      count > real_hand.count(card)):
                    no_rep = False
        if len(group) == 3 and no_rep:
            number_of_cards += 3
            two_groups_of_three.append(group)
    # when it is possible, create a list of plays in `full_turn`
    if number_of_cards == 6:
        to_group = len(table)
        for group in two_groups_of_three:
            for card in group:
                play = (active_player, 1, (card, to_group))
                full_turn.append(play)
            to_group += 1
        return True

    # check if it is possible to play 1 group of N from `hand`
    first_moves = []
    remaining_cards = real_hand.copy()
    table_copy = [[card for card in group] for group in table]
    to_group = len(table)
    for n in range(6, 2, -1):
        for group in groups_list:
            if len(group) == n:
                table_copy.append([])
                for card in group:
                    play = (active_player, 1, (card, to_group))
                    first_moves.append(play)
                    table_copy[to_group] += [card]
                    if card != 'XX':
                        remaining_cards.remove(card)
                break
        if first_moves:
            break

    # add the remaining cards to existing groups on `table`
    second_moves = []
    rem = 6 - len(first_moves)
    restart = True
    while restart:
        restart = False
        for card in remaining_cards.copy():
            if rem == 0:
                break
            for to_group in range(len(table_copy)):
                if valid_move(card, to_group, table_copy):
                    play = (active_player, 1, (card, to_group))
                    second_moves.append(play)
                    table_copy[to_group] += [card]
                    remaining_cards.remove(card)
                    rem -= 1
                    restart = True
                    break

    # move groups on `table` to add the last remaining cards
    # adjust the number of moves left as per the number of remaining cards
    if len(remaining_cards) * 2 < rem:
        rem = len(remaining_cards) * 2
    third_moves = []
    first_hand = remaining_cards
    first_table = table_copy
    for i in range(1, rem // 2):
        new_moves, new_hand, new_table = move_one_place_one(active_player,
                                                            first_hand,
                                                            first_table)
        third_moves += new_moves
        first_hand = new_hand
        first_table = new_table
        if not new_hand:
            break

    # when plays are possible, create a list of plays in `full_turn`
    if first_moves or second_moves or third_moves:
        full_turn = first_moves + second_moves + third_moves
        if third_moves and full_turn == third_moves:
            full_turn[0], full_turn[1] = full_turn[1], full_turn[0]
        return True

    return False


def bonus_play(play_history, active_player, hand, table):
    '''Returns the play as a 3-tuple given `play_history`- the combination of
    the plays made to date, `active_player`- the player whose turn it is to
    play, `hand`- the content of the player's hand and `table`- the groups on
    the table'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # get the number of the player preceding `active_player`
    if active_player == 0:
        preced_player = 3
    else:
        preced_player = active_player - 1
    # check if it is player's turn to play; if not, do not play
    if play_history:
        if not (play_history[-1][0] == preced_player and
                (play_history[-1][1] == 0 or play_history[-1][1] == 3) or
                play_history[-1][0] == active_player and
                (play_history[-1][1] == 1 or play_history[-1][1] == 2)):
            return

    # create a list of jokers in `hand`
    jokers = ['XX' for card in hand if card == 'XX']

    # create a list of cards in `hand` excluding jokers and sort it in
    # descending order as per `card_values`
    real_hand = hand.copy()
    for joker in jokers:
        real_hand.remove('XX')
    real_hand.sort(key=lambda x: values_dict[x[0]], reverse=True)

    # check if it is the opening turn and if it is the first play of the
    # opening turn
    opening_turn = True
    first_play_of_opening_turn = True
    for previous_play in play_history[::-1]:
        if previous_play[0] == active_player:
            if previous_play[1] == 1 or previous_play[1] == 2:
                first_play_of_opening_turn = False
            elif previous_play[1] == 3:
                opening_turn = False
                first_play_of_opening_turn = False
                break
    # check if it is the first play of a normal turn
    if play_history:
        first_play_of_normal_turn = True
        if (play_history[-1][0] == active_player and
                play_history[-1][1] == 1 or play_history[-1][1] == 2):
            first_play_of_normal_turn = False

    # when it is the first play of the opening turn
    if first_play_of_opening_turn:
        if opening_function(active_player, real_hand, table):
            return full_turn.pop(0)
        return (active_player, 0, None)
    # when it is the opening turn but not the first play
    elif opening_turn:
        if full_turn:
            return full_turn.pop(0)
        return (active_player, 3, None)
    # when it is the first play of a normal turn
    elif first_play_of_normal_turn:
        if normal_function(active_player, real_hand, jokers, table):
            return full_turn.pop(0)
        return (active_player, 0, None)
    # when it is a normal turn but not the first play
    else:
        if full_turn:
            return full_turn.pop(0)
        return (active_player, 3, None)
