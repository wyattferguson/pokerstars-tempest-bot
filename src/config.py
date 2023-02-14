from database import DB
import random
import time

DIR_PATH = 'C:\\Code\\poker\\src'

SUITS = ["s", "c", "h", "d"]
FACE_CARDS = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
ALL_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DECK = [f"{c}{s}" for s in SUITS for c in ALL_CARDS]

PRECISION = 3

DELAY_UPPER = 6.2
DELAY_LOWER = 0.4

POT_LOCATION = {
    'left': 580,
    'top': 280,
    'width': 125,
    'height': 32
}

WALLET_LOCATION = {
    'left': 600,
    'top': 670,
    'width': 150,
    'height': 25
}

CARD_OFFSET = 80
CARD_SUIT_Y_OFFSET = 35
CARD_SUIT_X_OFFSET = 5
CARD_SUIT_SQR = 15


CARD1_VALUE = {
    'left': 560,
    'top': 574,
    'width': 25,
    'height': 32
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
CARD_SUIT_LOCAIONS = [CARD1_SUIT]

SEAT_WIDTH = 150
SEAT_HEIGHT = 25

P1_SEAT = {
    'left': 55,
    'top': 510,
    'width': SEAT_WIDTH,
    'height': SEAT_HEIGHT
}

P2_SEAT = {
    'left': 100,
    'top': 240,
    'width': SEAT_WIDTH,
    'height': SEAT_HEIGHT
}

P3_SEAT = {
    'left': 545,
    'top': 154,
    'width': SEAT_WIDTH,
    'height': SEAT_HEIGHT
}

P4_SEAT = {
    'left': 1035,
    'top': 242,
    'width': SEAT_WIDTH,
    'height': SEAT_HEIGHT
}

P5_SEAT = {
    'left': 1080,
    'top': 510,
    'width': SEAT_WIDTH,
    'height': SEAT_HEIGHT
}

PLAYER_SEATS = [P1_SEAT, P2_SEAT, P3_SEAT, P4_SEAT, P5_SEAT]
