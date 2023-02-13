import sys

from pyautogui import hotkey

from config import *
from player import *


class Game():
    def __init__(self, testing: bool = True) -> None:
        self.testing = testing
        self.pot = 0
        self.wallet = 0
        self.blind = 0
        self.hand = []

    def next_hand(self):
        pass

    def random_delay(self):
        delay = round(random.uniform(DELAY_LOWER, DELAY_UPPER), 1)
        print(f"Delay -> {delay}s")
        if not self.testing:
            time.sleep(delay)

    def all_in(self):
        print("Move -> Push")
        if not self.testing:
            hotkey('ctrl', 'e')

    def fold(self):
        print("Move -> Fold")
        if not self.testing:
            hotkey('ctrl', 'f')


if __name__ == "__main__":
    '''
    # py game.py 1000 5

    wallet = int(sys.argv[1])
    blind = int(sys.argv[2])

    '''

    game = Game()
    game.random_delay()
