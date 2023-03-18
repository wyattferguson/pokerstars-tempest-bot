
from pathlib import Path

DIR_PATH = Path(__file__).parent

# GAME OPTIONS
TESTING = True  # toggle testing and logging
USE_KEYS = False  # toggle using shortcut keys in game

SMALL_BLIND = 1
HAND_WAGER = 10


ACTIONS = {
    # action : keyboard shortcut
    'call': ('ctrl', 'alt', 'c'),
    'fold': ('ctrl', 'alt', 'f')
}

# CARDS / DECK

SUITS = ["s", "c", "h", "d"]
ALL_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]


# TABLE

POT_LOCATION = {
    'left': 570,
    'top': 280,
    'width': 150,
    'height': 30
}


# CARD / SUIT

CARD_PATH = f"{DIR_PATH}\\needles\\"

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


# PLAYER

WALLET_LOCATION = {
    'left': 575,
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
