from database import DB
import random
import time


SUITS = ["s", "c", "h", "d"]
FACE_CARDS = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
ALL_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]

PRECISION = 3

DELAY_UPPER = 6.2
DELAY_LOWER = 0.4


SUIT_COLORS = {
    'c': (51, 153, 51),  # '339933' GREEN
    'h': (204, 0, 0),  # 'cc0000' RED
    's': (51, 51, 51),  # '333333' GREY
    'd': (0, 102, 204),  # '0066cc' BLUE
}

POT_LOCATION = {
    'left': 580,
    'top': 280,
    'width': 125,
    'height': 32
}

CARD1_VALUE = {
    'left': 550,
    'top': 560,
    'width': 23,
    'height': 30
}

CARD2_VALUE = {
    'left': 623,
    'top': CARD1_VALUE['top'],
    'width': CARD1_VALUE['width'],
    'height': CARD1_VALUE['height']
}

CARD1_SUIT = {
    'left': 555,
    'top': 595,
    'width': 8,
    'height': 8
}

CARD2_SUIT = {
    'left': 626,
    'top': CARD1_SUIT['top'],
    'width': 12,
    'height': 12
}

CARD_VALUE_LOCAIONS = [CARD1_VALUE, CARD2_VALUE]
CARD_SUIT_LOCAIONS = [CARD2_SUIT]
