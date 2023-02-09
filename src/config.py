import time

DATABASE = "../poker.db"

SUITS = ["s", "c", "h", "d"]
ALL_CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]

PRECISION = 3
