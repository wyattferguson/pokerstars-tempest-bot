

DATABASE = "./../poker.db"

PRECISION = 2

SUITS_INDEX = {"s": 0, "c": 1, "h": 2, "d": 3}
SUITS_SINGLE = ("s", "c", "h", "d")

CARDS_STR = "AKQJT98765432"

HAND_RANKINGS = ("High Card", "Pair", "Two Pair", "Three of a Kind",
                 "Straight", "Flush", "Full House", "Four of a Kind",
                 "Straight Flush", "Royal Flush")

CARD_VALUES = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
for card in range(2, 10):
    CARD_VALUES[str(card)] = card
