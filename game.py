from collections import namedtuple
import random
import pygame

Card = namedtuple('Card', ['rank', 'suit'])
pygame.display.init()

TARGET_SCORE = 50


class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '1']
    suits = ['spades', 'diamonds', 'clubs', 'hearts']

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]

    def __len__(self):
        return len(self.cards)

    def remove(self, card):
        """
        Removes given card from deck

        :param card: card object
        """
        self.cards.remove(card)

    def random_choice(self, game):
        """
        Selects a card at random from the card deck, returns that card and removes that card from the deck

        :return: card object
        """
        card = random.choice(game.cards)
        self.remove(card)
        return card

    @staticmethod
    def get_image(card):
        """
        Takes a card object and returns the corresponding image of that card

        :param card: card object (tup)
        :return: pygame surface
        """
        image = pygame.transform.scale(pygame.image.load(f"deck_images/{card.rank}_of_{card.suit}.png"), (70, 100))
        return image


class Game(Deck):
    def __init__(self, gid):
        super().__init__()
        self.gid = gid
        self.ready = False
        self.middle_card = self.random_choice(self)
        self.target_score = TARGET_SCORE
        self.p_scores = [0, 0]
        self.wins = [0, 0]
        self.active_p = random.choice([0, 1])
        self.turn = 0
        self.end_hands = {0: {"sets": None, "leftovers": None}, 1: {"sets": None, "leftovers": None}}
        self.deadwoods = {0: None, 1: None}
        self.win_round = {"win": False, "type": "", "player": None}
        self.ready_continue = [False, False]
        self.player_reset = [False, False]
        self.new_hands = []
        self.ready_new_game = [False, False]

    def next_turn(self):
        self.turn += 1

    def connected(self):
        """
        Returns whether the client is connected or not

        :return: bool
        """
        return self.ready

    def reset_round(self, player):
        """
        Resets the relevant attributes of the game object ready for starting a new round

        :param player: player object
        """
        self.active_p = random.choice([0, 1])
        self.turn = 0
        self.end_hands = {0: {"sets": None, "leftovers": None}, 1: {"sets": None, "leftovers": None}}
        self.deadwoods = {0: None, 1: None}
        self.win_round = {"win": False, "type": "", "player": self.win_round["player"]}
        self.ready_continue = [False, False]
        self.cards.clear()
        self.cards = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]
        self.new_hands = [player.deal_hand(self), player.deal_hand(self)]
        self.middle_card = self.random_choice(self)

    def new_game(self, player):
        """
        Resets game attributes for a new game

        :param player: player object
        """
        self.p_scores = [0, 0]
        winner = self.win_round["player"]
        winner_wins = self.wins[winner] + 1  # possibly undefined if no winner is set, which will never happen
        loser_wins = self.wins[1] if winner == 0 else self.wins[0]
        self.wins = [winner_wins, loser_wins] if winner == 0 else [loser_wins, winner_wins]
        self.reset_round(player)
        self.player_reset = [True, True]
        self.ready_new_game = [False, False]
