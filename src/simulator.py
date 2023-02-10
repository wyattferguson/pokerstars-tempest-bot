from config import *
from random import shuffle


class Player():
    def __init__(self) -> None:
        self.wallet = 100000
        self.bet = 200
        self.hand = []
        self.wins = 0
        self.hands_played = 0
        self.ties = 0
        self.losses = 0

    def new_hand(self, hand: list[str]):
        self.hand = hand

    def ante(self):
        pass

    def __str__(self) -> str:
        print(f"Wallet: {self.wallet} | Hands: {self.hands_played} | W: {self.wins} L: {self.losses} T: {self.ties}")


class Tempest():
    def __init__(self, players: int = 2) -> None:
        self.num_players = players
        self.players = [Player()] * players
        self.small_blind = 5
        self.big_blind = 2 * self.small_blind
        self.giant_blind = 2 * self.big_blind
        self.deck = []
        self.pot = 0

    def shuffle_deck(self):
        self.deck = DECK.copy
        shuffle(self.deck)

    def deal(self):
        self.shuffle_deck()
        pass

    def run(self):
        pass

    def determine_winner(self):
        pass


if __name__ == "__main__":
    pass
