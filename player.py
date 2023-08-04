from itertools import groupby
from operator import itemgetter
from game import Card


class Player:
    def __init__(self, pid, game):
        self.pid = pid
        self.selected_card = None  # stores card AND position of card
        self.swap = None
        self.hand = self.deal_hand(game)
        self.deadwood = 0
        self.sets = []
        self.runs = []
        self.score = 0
        self.ready = False

    def highest_playable_card(self):
        """
        Returns the highest ranked card not in a set or a run

        :return: card object
        """
        h = list(self.hand)
        sets_and_runs = self.sets + self.runs
        for card in sets_and_runs:
            if card in h:
                h.remove(card)
        try:
            max_card = max(h, key=lambda x: int(x.rank))
        except ValueError:
            max_card = Card(rank=0, suit=0)

        return max_card

    def update_deadwood(self):
        card_ranks = [11, 12, 13]
        sets_and_runs = set(self.sets + self.runs)
        dw = 0
        hpc = self.highest_playable_card()
        hand = list(self.hand)
        leftovers = [card for card in hand if card not in sets_and_runs]

        if leftovers:
            for card in leftovers:
                dw += 10 if int(card.rank) in card_ranks else int(card.rank)

        if (self.deadwood - int(hpc.rank)) <= 10 and len(self.hand) == 11:  # used for when a player can press a win button
            dw = dw - (10 if int(hpc.rank) > 10 else int(hpc.rank))

        if dw < 0:
            dw = 0

        self.deadwood = dw

    def update_sets_and_runs(self):
        sets = self.is_set(self.hand)[0]
        runs = self.is_run(self.hand)
        self.sets, self.runs = self.handle_sets_using_same_card(sets, runs)

    def handle_sets_using_same_card(self, sets, runs):
        """
        Removes any sets that are using the same card in the given players hand and returns a revised list of sets

        :param player: player object
        :param sets: list
        :param runs: list
        :return list
        """
        groups = self.is_set(self.hand)[1]

        group_to_remove = None
        for card in sets + runs:
            if card in sets and card in runs and len(groups[card.rank]) < 4:
                group_to_remove = groups[card.rank]
        if group_to_remove is not None:
            for card in group_to_remove:
                if card in sets:
                    sets.remove(card)
                elif card in runs:
                    runs.remove(card)

        return sets, runs

    def deal_hand(self, game):
        """
        Deals and sorts the hand of a player

        :return: sorted hand
        """
        hand = []
        for card in range(1, 11):
            hand.append(game.random_choice(game))

        return self.sort_hand(hand)

    def reset_player(self, game, player):
        """
        Resets the relevant attributes of the player for starting a new round

        :param game: game object
        :param player: player object
        """
        self.selected_card = None  # stores card and position of card
        self.swap = None
        self.deadwood = 0
        self.hand = game.new_hands[player.pid]
        self.sets = []
        self.runs = []
        self.ready = False
        self.score = game.p_scores[player.pid]

    @staticmethod
    def is_set(hand):
        """
        Takes in a list of cards and returns a list of all cards that are in a set of 3 or more. Also returns variable
        'groups' for use in 'highlight_cards' function
        :param hand: list of card objects
        :return: list of card objects, groups
        """
        h = hand
        group_by = groupby(h, lambda x: x.rank)
        keys_added = []
        groups = {}
        for k, g in group_by:
            l = list(g)
            if k in keys_added and len(l) < 3:
                pass
            else:
                keys_added.append(k)
                groups[k] = l
        set_cards = [c for k in groups if len(groups[k]) > 2 for c in groups[k]]

        return set_cards, groups

    @staticmethod
    def is_run(hand):
        """
        Returns a list of the cards in a run of 3 or more from hand
        :param hand: list of card objects
        :return: list of card objects
        """

        # Taken from the 'moreitertools' package. Modified for use with card objects
        def consecutive_groups(iterable, ordering=lambda x: x):
            for k, g in groupby(
                    enumerate(iterable), key=lambda x: x[0] - int(ordering(x[1].rank))
            ):
                yield map(itemgetter(1), g)

        h = hand
        potentials = []

        for i, card in enumerate(h):
            try:
                if h[i].suit == h[i + 1].suit:
                    potentials.append(h[i])
                elif h[i].suit == h[i - 1].suit:
                    potentials.append(h[i])
                    potentials.append(Card(rank="-1", suit="joker"))  # used to break up runs
            except IndexError:
                if h[i].suit == h[i - 1].suit:
                    potentials.append(h[i])
                    break

        run_cards = []
        for group in consecutive_groups(potentials):
            group_list = list(group)
            for c in group_list:
                if len(group_list) > 2:
                    run_cards.append(c)

        return run_cards

    @staticmethod
    def sort_hand(hand):  # could add sorting by suit instead of just rank
        """
        Sorts the given players hand
        :return: sorted hand (list)
        """
        return sorted(hand, key=lambda x: int(x.rank), reverse=False)
