

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
