import time
import random

DATABASE = "../poker.db"

from database import DB

SUITS = ["s", "c", "h", "d"]
FACE_CARDS = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
ALL_CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]

PRECISION = 3

DELAY_UPPER = 6.2
DELAY_LOWER = 0.4
