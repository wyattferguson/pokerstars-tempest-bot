"""
Add Shortcut Keys:
CTRL + ALT + F = FOLD
CTRL + ALT + C = CALL

"""

import keyboard
from pyautogui import hotkey
import logging

from config import *
from vision import Vision


class Game():
    def __init__(self, delay: int = 1, small_blind: int = 500, wager: int = 20000,
                 wallet: int = 200000, testing: bool = True) -> None:
        self.delay = delay
        self.players = 0
        self.pot = 0
        self.hand = []
        self.games = 0
        self.testing = testing
        self.wager = wager
        self.sb = small_blind
        self.bb = 2 * self.sb
        self.gb = 2 * self.bb
        self.action_option = 'push'
        self.wallet = wallet
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
                self.action_option = self.vsn.read_players()
                self.pot = self.vsn.read_pot()
                self.wallet = self.vsn.read_wallet()
                self.player_pushed, self.players = self.vsn.read_players()
                print(self)

            time.sleep(self.delay)

    def random_delay(self) -> None:
        delay = round(random.uniform(DELAY_LOWER, DELAY_UPPER), 1)
        print(f"Delay -> {delay}s")
        if not self.testing:
            time.sleep(delay)

    def fold(self) -> None:
        self.action = "fold"
        print("Action -> Folding")
        if not self.testing:
            pass

    def call(self) -> None:
        self.action = "call"
        print("Action -> Calling")
        if not self.testing:
            pass

    def player_action(self) -> None:
        mults = self.wager / self.gb
        stack = self.round_decimal(mults, 0.05)
        nash_row = self.db.get_nash(stack, self.action_option, self.hand)
        print(nash_row)
        if not self.testing:
            self.random_delay()

        if nash_row['score'] >= 0.5:
            self.call()
        else:
            self.fold()

    def round_decimal(self, num, decimal) -> float:
        return round(num / decimal) * decimal

    def __str__(self) -> str:
        game_state = f"POT: {self.pot} | PLYS: {self.players} | WLT: {self.wallet} | GMS: {self.games} | HND: {self.hand} | OPT: {self.action_option} | ACT: {self.action}"
        self.logger.info(game_state)
        return game_state


if __name__ == "__main__":
    delay = 2
    testing = True
    play = Game(delay, 5, 200, 2000, testing)
    play.hand = ['Ts', 'Js']
    play.player_pushed = 'call'
    play.player_action()
    # play.run(delay)
