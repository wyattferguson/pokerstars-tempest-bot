
import random
import time
from pathlib import Path

DIR_PATH = Path(__file__).parent

# game options
PLAYER_SEAT = 0  # 0 -> 3, 0 center, then clock wise
TESTING = True  # toggle testing and logging
BLUFFING = False  # toggle use of bluffing
USE_KEYS = False  # toggle using shortcut keys in game
LIVE_PLAY = False

BLUFF_RATE = 1  # 0 (never) -> 10 (always)
BLUFF_MIN = 0.43  # minimum hand strength to bluff

DELAY_UPPER = 3.2  # upper time bound to delay action on screen
DELAY_LOWER = 0.6  # lower bound for action on screen

# card / deck generation

SUITS = ["s", "c", "h", "d"]
FACE_CARDS = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
ALL_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]

PRECISION = 3


# TABLE
WINDOW_Y = 244
WINDOW_X = 0

PLAYER_SEATS = [
    (550, 788),  # bottom
    (23, 433),  # left
    (555, 182),  # top
    (1100, 445),  # right
]

PLAYER_LOC = {
    'left': PLAYER_SEATS[PLAYER_SEAT][0] + WINDOW_X,
    'top': PLAYER_SEATS[PLAYER_SEAT][1] + WINDOW_Y,
}

POT_LOCATION = {
    'left': 550 + WINDOW_X,
    'top': 327 + WINDOW_Y,
    'width': 180,
    'height': 28
}


# CARD / SUIT LOCATIONS

CARD1_VALUE = {
    'left': PLAYER_LOC['left'] + 10,
    'top': PLAYER_LOC['top'] - 115,
    'width': 30,
    'height': 40
}

CARD1_SUIT = {
    'left': PLAYER_LOC['left'] + 12,
    'top': PLAYER_LOC['top'] - 77,
    'width': 35,
    'height': 35
}


CARD2_VALUE = {
    'left': PLAYER_LOC['left'] + 80,
    'top': PLAYER_LOC['top'] - 120,
    'width': 35,
    'height': 40
}

CARD2_SUIT = {
    'left': PLAYER_LOC['left'] + 78,
    'top': PLAYER_LOC['top'] - 82,
    'width': 35,
    'height': 35
}

CARD_VALUE_LOCAIONS = [CARD1_VALUE, CARD2_VALUE]
CARD_SUIT_LOCAIONS = [CARD1_SUIT, CARD2_SUIT]


# player info

WALLET_LOCATION = {
    'left': PLAYER_LOC['left'] + 20,
    'top': PLAYER_LOC['top'] + 38,
    'width': 140,
    'height': 28
}

TIMER_LOCATION = {
    'left': PLAYER_LOC['left'],
    'top': PLAYER_LOC['top'] + 70,
    'width': 150,
    'height': 15
}
