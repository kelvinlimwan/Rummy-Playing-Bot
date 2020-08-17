from valid_table import n_of_a_kind, run
from valid_play import valid_move

full_turn = []  # global variable

def create_groups_list(hand):
    '''Returns a list of all possible N-of-a-kind groups and run groups that
    can be created from `hand` sorted in descending order of group sizes'''

    card_values = 'A234567890JQK'

    groups_list = []
    # add N-of-a-kind groups
    group = [hand[0]]
    mod_hand = hand + ['ZZ']
    for card in mod_hand[1:]:
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
            if len(group) >= 3:
                groups_list.append(group)
            group = [card]

    # add run groups
    hand_copy = hand.copy()
    for anchor_card in hand:
        if anchor_card in hand_copy:
            group = [anchor_card]
            hand_copy.remove(anchor_card)
            for card in hand_copy:
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
            if len(group) >= 3:
                for card in group[1:]:
                    hand_copy.remove(card)
                groups_list.append(group)

    return sorted(groups_list, key=len, reverse=True)

def move_one_place_one(active_player, hand, table):
    '''Returns a list of two valid moves for `active_player` to move a card
    from a group on the `table` to another and then place a card from `hand` in
    a group, a list of groups in the new table and a list of card in the new
    hand'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    new_moves = []
    new_table = []
    new_hand = []
    for anchor_group in table:
        from_group = table.index(anchor_group)
        # when `anchor_group` is N-of-a-kind
        if n_of_a_kind(anchor_group):
            iterator = set(anchor_group)
        # when `anchor_group` is a run
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
                    # for each card in `hand`
                    for place_card in hand:
                        # check if `place_card` can be moved to the
                        # `anchor_group`; if so, update `new_moves`,
                        # `new_table` and `new_real_hand`
                        if valid_move(place_card, from_group, table_copy2):
                            play1 = (active_player, 2, (move_card, from_group,
                                                        to_group))
                            play2 = (active_player, 1, (place_card,
                                                        from_group))
                            new_moves = [play1, play2]
                            new_table = table_copy2
                            new_table[from_group] += [place_card]
                            new_hand = hand.copy()
                            new_hand.remove(place_card)
                            return new_moves, new_hand, new_table
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
                            new_hand = hand.copy()
                            new_hand.remove(place_card)
                            return new_moves, new_hand, new_table

    return new_moves, new_hand, new_table


def opening_function(active_player, hand, table):
    '''Returns True and creates a list of plays in `full_turn` when the
    opening turn can be played given `active_player`, `hand` and `table`, and
    False otherwise'''

    # dictionary of card values, each assigned to a point number
    card_values = 'A234567890JQK'
    values_dict = dict(zip(card_values, range(1, 14)))

    # use global variable
    global full_turn

    # compute the total points of the six highest cards in `hand` and check if
    # it is less than 24; if so, pick a card
    max_opening_points = 0
    for card in hand[:6]:
        max_opening_points += values_dict[card[0]]
    if max_opening_points < 24:
        return False

    # list of all possible N-of-a-kind groups and run groups that can be
    # created from `hand`
    groups_list = create_groups_list(hand)

    # list of 2-tuples with each group and their points and sorted in
    # descending order of points
    points_list = []
    for group in groups_list:
        points = 0
        for card in group:
            points += values_dict[card[0]]
        points_list.append((group, points))
    points_list.sort(key=lambda x: x[1], reverse=True)

    # check if it is possible to play 2 groups of 3 from `hand` and if the
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
                if card in group and count > hand.count(card):
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

    # check if it is possible to play 1 group of N from `hand`
    points_of_play = 0
    first_moves = []
    remaining_cards = hand.copy()
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


def normal_function(active_player, hand, table):
    '''Returns True and creates a list of plays in `full_turn` when a
    normal turn can be played given `active_player`, `hand` and `table`, and
    False otherwise'''

    # use global variable
    global full_turn

    # list of all possible N-of-a-kind groups and run groups that can be
    # created from `hand`
    groups_list = create_groups_list(hand)

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
                if card in group and count > hand.count(card):
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
    remaining_cards = hand.copy()
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


def play(play_history, active_player, hand, table):
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

    # sort `hand` in descending order as per `card_values`
    hand.sort(key=lambda x: values_dict[x[0]], reverse=True)

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
        if opening_function(active_player, hand, table):
            return full_turn.pop(0)
        return (active_player, 0, None)
    # when it is the opening turn but not the first play
    elif opening_turn:
        if full_turn:
            return full_turn.pop(0)
        return (active_player, 3, None)
    # when it is the first play of a normal turn
    elif first_play_of_normal_turn:
        if normal_function(active_player, hand, table):
            return full_turn.pop(0)
        return (active_player, 0, None)
    # when it is a normal turn but not the first play
    else:
        if full_turn:
            return full_turn.pop(0)
        return (active_player, 3, None)
