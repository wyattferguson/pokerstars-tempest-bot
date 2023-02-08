

SUITS = ["s", "c", "h", "d"]
CARDS = "AKQJT98765432"

HAND_RANKINGS = ("High Card", "Pair", "Two Pair", "Three of a Kind",
                 "Straight", "Flush", "Full House", "Four of a Kind",
                 "Straight Flush", "Royal Flush")

CARD_VALUES = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
for card in range(2, 10):
    CARD_VALUES[str(card)] = card
