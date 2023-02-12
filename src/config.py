from database import DB
import random
import time

DATABASE = "../poker.db"


SUITS = ["s", "c", "h", "d"]
FACE_CARDS = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
ALL_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]

PRECISION = 3

DELAY_UPPER = 6.2
DELAY_LOWER = 0.4
