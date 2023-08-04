def pass_btn_func(**kwargs):
    player, n = kwargs["player"], kwargs["n"]
    n.send_string_receive_game("pass")


def sort_btn_func(**kwargs):
    player, n = kwargs["player"], kwargs["n"]
    player.hand = player.sort_hand(player.hand)
    player.selected_card = None


def m_card_func(**kwargs):
    player, n = kwargs["player"], kwargs["n"]
    card = n.send_string_receive_card("m_card")
    player.hand.append(card)


def deck_func(**kwargs):
    player, n, game = kwargs["player"], kwargs["n"], kwargs["game"]
    if len(game.cards) == 0:
        n.send_string_receive_game("reset")
    else:
        card = n.send_string_receive_card("deck")
        player.hand.append(card)


def play_func(**kwargs):
    player, n = kwargs["player"], kwargs["n"]
    if player.selected_card:
        player.hand.remove(player.selected_card[0])
        n.send_string_receive_game(f"play {player.selected_card[0].rank} {player.selected_card[0].suit}")
        player.selected_card = None


def ready_func(**kwargs):
    player, n = kwargs["player"], kwargs["n"]
    player.ready = True
    n.send_string_receive_game(f"ready {player.score}")


def new_game_ready_func(**kwargs):
    n, game = kwargs["n"], kwargs["game"]
    n.send_string_receive_game("new_game_ready")
