
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
POT_LOCATION = {
    'left': 570,
    'top': 280,
    'width': 150,
    'height': 30
}


# CARD / SUIT LOCATIONS

CARD_PATH = f"{DIR_PATH}\\needles\\pokerstars\\"

CARD_OFFSET = 83
CARD_SUIT_Y_OFFSET = 33
CARD_SUIT_X_OFFSET = 0
CARD_SUIT_SQR = 20

CARD1_VALUE = {
    'left': 562,
    'top': 570,
    'width': 22,
    'height': 30
}

CARD2_VALUE = {
    'left': CARD1_VALUE['left'] + CARD_OFFSET,
    'top': CARD1_VALUE['top'],
    'width': CARD1_VALUE['width'],
    'height': CARD1_VALUE['height']
}

CARD1_SUIT = {
    'left': CARD1_VALUE['left'] + CARD_SUIT_X_OFFSET,
    'top': CARD1_VALUE['top'] + CARD_SUIT_Y_OFFSET,
    'width': CARD_SUIT_SQR,
    'height': CARD_SUIT_SQR
}

CARD2_SUIT = {
    'left': CARD1_SUIT['left'] + CARD_OFFSET,
    'top': CARD1_SUIT['top'],
    'width': CARD_SUIT_SQR,
    'height': CARD_SUIT_SQR
}

CARD_VALUE_LOCAIONS = [CARD1_VALUE, CARD2_VALUE]
CARD_SUIT_LOCAIONS = [CARD1_SUIT, CARD2_SUIT]


# player info

WALLET_LOCATION = {
    'left': 600,
    'top': 670,
    'width': 150,
    'height': 25
}

TIMER_LOCATION = {
    'left': WALLET_LOCATION['left'] - 50,
    'top': WALLET_LOCATION['top'] + 32,
    'width': 100,
    'height': 25
}
