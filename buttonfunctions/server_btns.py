import pickle
from game import Card


def convert_string(data, player):
    """
    Converts the string data of a players hand to 2 lists of card objects and returns them
    :param data: string
    :return: list, list
    """
    data = data.split(' ')
    string_hand = data[2:12] if len(player.hand) == 10 else data[2:13]
    sets_and_runs = data[12:]
    leftovers = []
    sets_and_runs_obj = []
    if "None" not in sets_and_runs:
        for card in sets_and_runs:
            card = card.split('_')
            sets_and_runs_obj.append(Card(rank=card[0], suit=card[1]))

    for card in string_hand:
        if card in sets_and_runs or card == "None":
            pass
        else:
            card = card.split('_')
            leftovers.append(Card(rank=card[0], suit=card[1]))
    return sets_and_runs_obj, leftovers


def pass_btn(**kwargs):
    game = kwargs["game"]
    game.active_p = not game.active_p
    game.turn += 1


def middle_card(**kwargs):
    game, conn = kwargs["game"], kwargs["conn"]
    card = game.middle_card
    conn.sendall(pickle.dumps(card))
    game.middle_card = None


def deck(**kwargs):
    game, conn = kwargs["game"], kwargs["conn"]
    if len(game.cards) == 0:
        pass
    else:
        card = game.random_choice(game)
        conn.sendall(pickle.dumps(card))


def reset(**kwargs):
    game, player = kwargs["game"], kwargs["player"]
    game.reset_round(player)
    game.player_reset = [True, True]


def change_reset(**kwargs):
    game, player = kwargs["game"], kwargs["player"]
    game.player_reset[player.pid] = False


def play_btn(**kwargs):
    game, data = kwargs["game"], kwargs["data"]
    game.active_p = not game.active_p
    game.turn += 1
    rank, suit = data[5:].split(' ')
    game.middle_card = Card(rank, suit)


def win_btn(**kwargs):
    game, data, player = kwargs["game"], kwargs["data"], kwargs["player"]
    game.win_round["win"] = True
    game.win_round["type"] = data[4:]
    game.win_round["player"] = player.pid


def hand(**kwargs):
    game, data, player = kwargs["game"], kwargs["data"], kwargs["player"]
    game.end_hands[player.pid]["sets"], game.end_hands[player.pid]["leftovers"] = convert_string(
        data, player)
    if player.pid == 0:
        game.deadwoods[0] = data.split(' ')[1]
    else:
        game.deadwoods[1] = data.split(' ')[1]


def ready(**kwargs):
    game, data, player = kwargs["game"], kwargs["data"], kwargs["player"]
    game.ready_continue[player.pid] = True
    game.p_scores[player.pid] += int(data.split(' ')[1])


def reset_ready(**kwargs):
    game = kwargs["game"]
    game.ready_continue = [False, False]


def new_game_ready(**kwargs):
    game, player = kwargs["game"], kwargs["player"]
    game.ready_new_game[player.pid] = True


def new_game(**kwargs):
    game, player = kwargs["game"], kwargs["player"]
    if game.win_round["win"]:
        game.new_game(player)
