"""
Used to store all the conditions needed for the player to press a button
"""


class Conditions:
    def __init__(self, game, player):
        self.active_player = game.active_p == player.pid
        self.turn = game.turn
        self.in_hand_10 = len(player.hand) == 10
        self.in_hand_11 = len(player.hand) == 11
        self.card_selected = True if player.selected_card else False
        self.middle_card = True if game.middle_card else False
        self.end_game = True if game.win_round["win"] else False
        self.continue_clicked = False if player.ready else True
        self.card_ranks = [11, 12, 13]
        self.knock_condition = player.deadwood > 0 <= 10
        self.super_condition = sorted(player.hand) == sorted(player.sets + player.runs)  # efficiency?
        self.gin_condition = player.deadwood <= 0 and not self.super_condition
        self.not_ready = not game.ready_new_game[player.pid]
        self.winning_score = True if True in (score >= game.target_score for score in game.p_scores) else False