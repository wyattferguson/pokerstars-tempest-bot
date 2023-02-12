from itertools import combinations, product
from random import sample, shuffle

import poker_hand
from config import *
from player import *


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
            print(f"Game #{n+1}")
            self.deal_cards()
            self.player_actions()
            winners = self.determine_winners()

            pot_divide = len(winners)
            player_payout = round(self.pot / pot_divide, 2)
            for winner in winners:
                player = self.players[winner[0]]
                player.win(player_payout)

                print("Winning Hand: ", winner[1])
                print("Winner: ", player)

    def deal_cards(self):
        self.blinds = [self.blinds[-1]] + self.blinds[:-1]  # cycle blinds

        self.board.clear()
        shuffle(self.deck)

        dealt_cards = sample(self.deck, (2 * self.player_count) + 5)
        for i, p in enumerate(self.players):
            p.new_hand([dealt_cards.pop(n) for n in range(2)], self.blinds[i])
            p.hand.sort()

        self.board.extend(dealt_cards)
        self.board.sort()

    def player_actions(self):
        for player in self.players:
            player.move()

    def payout_winners(self):
        pass

    def get_antes(self):
        pass

    def determine_winners(self):
        highest_hands = []
        for player in self.players:
            if player.is_playing():
                card_pool = self.board.copy()
                card_pool.extend(player.hand)
                card_combinations = [list(cards)
                                     for cards in combinations(card_pool, 5)]
                highest_hands.append(max([poker_hand.Hand(h)
                                          for h in card_combinations]))
        winning_hand = max(highest_hands)

        winners = []
        for player in range(highest_hands.count(winning_hand)):
            idx = highest_hands.index(winning_hand)
            winners.append((idx, highest_hands.pop(idx)))
        return winners

    def __str__(self):
        board = ""
        for c in self.board:
            board += str(FACE_CARDS.get(c.rank, c.rank)) + c.suit + " "
        rv = "-" * 40 + f"\n\nCommunity Cards:\n{board}\n" + "*" * 20 + "\n"
        for ct, player in enumerate(self.players):
            player_cards = ""
            for c in player.hand:
                player_cards += str(FACE_CARDS.get(c.rank,
                                    c.rank)) + c.suit + " "
            rv += f"Player {str(ct)}: {player_cards}\n"
        winners = self.determine_winners()
        rv += "*" * 20 + "\n"
        for winner in winners:
            rv += f"Player {str(winner[0])} wins: {str(winner[1])}\n"
        rv += "\n" + "-" * 40
        return rv


if __name__ == "__main__":
    games = 1
    players = [Chaos("P1"), Chaos("P2"), Chaos("P3")]
    small_blind = 5
    th = PushFold(players, small_blind)
    th.play(games)
