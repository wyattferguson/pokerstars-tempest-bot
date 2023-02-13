from itertools import combinations, product
from random import sample, shuffle

import poker_hand
from config import *
from player import *

'''
FIXES
- Player must check if broke before receiving cards
'''


class PushFold():
    def __init__(self, players: list, small_blind: int = 5):
        self.player_count = len(players)
        self.players = players
        self.board = []
        self.pot = 0
        self.small_blind = small_blind
        self.big_blind = 2 * self.small_blind
        self.giant_blind = 2 * self.big_blind
        self.blinds = [self.small_blind, self.big_blind, self.giant_blind]
        self.deck = [poker_hand.Card(*c)
                     for c in product(poker_hand.SUITS, poker_hand.RANKS)]

    def play(self, games: int = 1):
        for n in range(games):
            print(f"\n########## Game #{n+1} ##########")
            self.deal_cards()
            print(f"Pot -> {self.pot}")
            self.player_actions()
            print(self)

            winners = self.determine_winners()
            self.payout_winners(winners)

    def deal_cards(self):
        # clear board and shuffle deck
        self.pot = 0
        self.board.clear()
        shuffle(self.deck)

        # shift blinds
        self.players = [self.players[-1]] + self.players[:-1]

        # deal player cards
        dealt_cards = sample(self.deck, (2 * self.player_count) + 5)
        is_small_blind = True
        for i, p in enumerate(self.players):
            p.new_hand([dealt_cards.pop(n) for n in range(2)], self.blinds[i], is_small_blind)
            p.hand.sort()
            is_small_blind = False
            self.pot += p.blind

        # deal board cards
        self.board.extend(dealt_cards)
        self.board.sort()

    def player_actions(self):
        first_call = True
        last_player = False
        for i, player in enumerate(self.players):
            if first_call and i == self.player_count - 1:
                last_player = True

            action = player.move(first_call, last_player)
            if action > 0:
                first_call = False
            print(player)
            self.pot += action

    def payout_winners(self, winners):
        pot_divide = len(winners)
        player_payout = round(self.pot / pot_divide, 2)
        print(f"Game -> {pot_divide} Winners | {player_payout} Payout")

        for winner in winners:
            winner.win(player_payout)

    def determine_winners(self):
        highest_hands = []
        for player in self.players:
            if player.playing:
                card_pool = self.board.copy()
                card_pool.extend(player.hand)
                card_combinations = [list(cards)
                                     for cards in combinations(card_pool, 5)]
                max_hand = max([poker_hand.Hand(h)
                                for h in card_combinations])
                player.hand = max_hand.list_format()
                highest_hands.append(max_hand)

        winning_hand = max(highest_hands)
        winners = []
        for player in self.players:
            if player.hand == winning_hand.list_format():
                winners.append(player)
        return winners

    def __str__(self):
        board = ""
        for c in self.board:
            board += str(FACE_CARDS.get(c.rank, c.rank)) + c.suit + " "
        return f"Board -> {board}| {round(self.pot,2)} Pot"


if __name__ == "__main__":
    games = 3
    players = [Chaos("GG"), Chaos("XX"), Chaos("BB")]
    small_blind = 5
    th = PushFold(players, small_blind)
    th.play(games)
