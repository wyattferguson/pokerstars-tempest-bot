"""
Shortcut Keys:
CTRL + ALT + F = FOLD
CTRL + ALT + C = CALL

- Figure out nash stack calculation
- Add hand wallet

"""

import keyboard
from pyautogui import hotkey
import logging

from config import *
from vision import Vision


class Game():
    def __init__(self, delay: int = 1) -> None:
        self.delay = delay
        self.players = 0
        self.pot = 0
        self.hand = []
        self.games = 0
        self.player_pushed = False
        self.wallet = 1000
        self.hand_wallet = 0  # FIGURE THIS OUT
        self.action = False
        self.vsn = Vision()
        self.db = DB()
        self.logger = logging.getLogger()
        self.setup_logging()

    def setup_logging(self):
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(message)s')
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def run(self) -> None:
        # print("Press 's' to start playing.")
        # keyboard.wait('s')
        while True:

            new_hand = self.vsn.cards()
            if new_hand and new_hand != self.hand and len(new_hand) == 2:
                print(f"New Hand -> {new_hand}")
                self.hand = new_hand
                self.games += 1
                self.call = self.vsn.read_players()
                self.pot = self.vsn.read_pot()
                self.wallet = self.vsn.read_wallet()
                self.player_pushed, self.players = self.vsn.read_players()
                print(self)

            time.sleep(self.delay)

    def random_delay(self):
        delay = round(random.uniform(DELAY_LOWER, DELAY_UPPER), 1)
        print(f"Delay -> {delay}s")
        if not self.testing:
            time.sleep(delay)

    def player_action(self) -> None:
        stack = 1.0
        nash_row = self.db.get_nash(stack, self.player_pushed, self.hand)
        print(nash_row)
        self.action = "Push"
        # ADD TAKE ACTION HERE AFTER RADOM DELAY
        self.random_delay()

    def __str__(self) -> str:
        game_state = f"POT: {self.pot} | PLYS: {self.players} | WLT: {self.wallet} | GMS: {self.games} | HND: {self.hand} | CLD: {self.player_pushed} | ACT: {self.action}"
        self.logger(game_state)
        return game_state


if __name__ == "__main__":
    delay = 2

    play = Game()
    play.run(delay)
