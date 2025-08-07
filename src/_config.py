from pathlib import Path

from _types import Card, Location

DIR_PATH = Path(__file__).parent

# GAME OPTIONS
TESTING: bool = True  # toggle testing and logging
USE_KEYS: bool = False  # toggle using shortcut keys in game

SMALL_BLIND: int = 1
HAND_WAGER: int = 10
MAX_STACK: int = 200
CALL_THRESHOLD: float = 0.5

ACTIONS: dict[str, tuple[str, str, str]] = {
    # action : keyboard shortcut
    "call": ("ctrl", "alt", "c"),
    "fold": ("ctrl", "alt", "f"),
}

# CARDS / DECK

SUITS = ["s", "c", "h", "d"]
ALL_CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
DECK = [Card(value=value, suit=suit) for suit in SUITS for value in ALL_CARDS]


# TABLE

POT_LOCATION: Location = Location(
    x=570,
    y=280,
    width=150,
    height=30,
)


# CARD / SUIT

CARD_PATH: str = f"{DIR_PATH}\\needles\\"

CARD_OFFSET: int = 83
CARD_SUIT_Y_OFFSET: int = 33
CARD_SUIT_X_OFFSET: int = 0
CARD_SUIT_SQR: int = 20

CARD1_VALUE: Location = Location(
    x=562,
    y=570,
    width=22,
    height=30,
)

CARD2_VALUE: Location = Location(
    x=CARD1_VALUE.x + CARD_OFFSET,
    y=CARD1_VALUE.y,
    width=CARD1_VALUE.width,
    height=CARD1_VALUE.height,
)

CARD1_SUIT: Location = Location(
    x=CARD1_VALUE.x + CARD_SUIT_X_OFFSET,
    y=CARD1_VALUE.y + CARD_SUIT_Y_OFFSET,
    width=CARD_SUIT_SQR,
    height=CARD_SUIT_SQR,
)

CARD2_SUIT: Location = Location(
    x=CARD1_SUIT.x + CARD_OFFSET,
    y=CARD1_SUIT.y,
    width=CARD_SUIT_SQR,
    height=CARD_SUIT_SQR,
)

HAND = [
    {
        "value": CARD1_VALUE,
        "suit": CARD1_SUIT,
    },
    {
        "value": CARD2_VALUE,
        "suit": CARD2_SUIT,
    },
]

# PLAYER

WALLET_LOCATION: Location = Location(
    x=575,
    y=670,
    width=150,
    height=25,
)

TIMER_LOCATION: Location = Location(
    x=WALLET_LOCATION.x - 50,
    y=WALLET_LOCATION.y + 32,
    width=100,
    height=25,
)
