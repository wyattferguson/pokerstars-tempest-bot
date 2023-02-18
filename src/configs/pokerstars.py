
# TABLE POT

POT_LOCATION = {
    'left': 580,
    'top': 280,
    'width': 125,
    'height': 32
}


# CARD / SUIT LOCATIONS

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


# ALL PLAYER WALLET BOXES / SEATS

SEAT_WIDTH = 150
SEAT_HEIGHT = 25

WALLET_LOCATION = {
    'left': 600,
    'top': 670,
    'width': SEAT_WIDTH,
    'height': SEAT_HEIGHT
}

TIMER_LOCATION = {
    'left': WALLET_LOCATION['left'] - 50,
    'top': WALLET_LOCATION['top'] + 32,
    'width': 100,
    'height': 25
}

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
