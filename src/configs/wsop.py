
# TABLE
WINDOW_Y = 244
WINDOW_X = 0

PLAYER_LOC = {
    'left': 550 + WINDOW_X,
    'top': 790 + WINDOW_Y,
}

POT_LOCATION = {
    'left': 550 + WINDOW_X,
    'top': 327 + WINDOW_Y,
    'width': 180,
    'height': 28
}


# CARD / SUIT LOCATIONS

CARD_PATH = f"{DIR_PATH}\\needles\\wsop\\"

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
