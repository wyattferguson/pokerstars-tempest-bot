from config import *


class Card:
    # Takes in strings of the format: "As", "Tc", "6d"
    def __init__(self, card_string):
        card_index, self.suit = card_string[0], card_string[1]

        self.value = CARD_VALUES[card_index]
        self.suit_index = SUITS.index(self.suit)
        #print(card_index, self.suit, self.suit_index)

    def __str__(self):
        return CARDS[14 - self.value] + self.suit

    def __repr__(self):
        return CARDS[14 - self.value] + self.suit

    def __eq__(self, other):
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.value == other.value and self.suit == other.suit
