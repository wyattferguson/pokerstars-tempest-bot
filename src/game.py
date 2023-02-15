
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
        self.opp_pushed = False
        self.wallet = wallet
        self.action = False
        self.vsn = Vision()
        self.db = DB()
        self.logger = logging.getLogger()
        self.setup_logging()

    def setup_logging(self):
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def run(self) -> None:
        while True:
            # wait for timer to appear
            print("Waiting...")
            if not self.testing:
                while not self.vsn.read_timer():
                    time.sleep(1)

            # read new cards
            new_hand = self.vsn.cards()
            if new_hand and new_hand != self.hand and len(new_hand) == 2:
                print(f"New Hand -> {new_hand}")
                self.hand = new_hand
                self.games += 1
                self.pot = self.vsn.read_pot()
                self.opp_pushed, self.players = self.vsn.read_players()
                self.strategy()
                print(self)

            time.sleep(self.delay)
            self.wallet = self.vsn.read_wallet()

    def random_delay(self) -> None:
        delay = round(random.uniform(DELAY_LOWER, DELAY_UPPER), 1)
        print(f"Delay -> {delay}s")
        if not self.testing:
            time.sleep(delay)

    def fold(self) -> None:
        self.action = "fold"
        print("Action -> Folding")
        if not self.testing:
            hotkey('ctrl', 'alt', 'f')

    def push_allin(self) -> None:
        self.action = "call"
        print("Action -> Calling")
        if not self.testing:
            hotkey('ctrl', 'alt', 'c')

    def strategy(self) -> None:
        mults = self.wager / self.gb
        stack = self.round_decimal(mults, 0.05)
        status = "call" if self.opp_pushed else "push"
        nash_row = self.db.get_nash(stack, status, self.hand)

        if not self.testing:
            self.random_delay()

        if nash_row['score'] >= 0.5:
            self.push_allin()
        else:
            self.fold()

    def round_decimal(self, num, decimal) -> float:
        return round(num / decimal) * decimal

    def __str__(self) -> str:
        game_state = f"POT: {self.pot} | PLYS: {self.players} | WLT: {self.wallet} | GMS: {self.games} | HND: {self.hand} | OPP: {self.opp_pushed} | ACT: {self.action}"
        if not self.testing:
            self.logger.info(game_state)
        return game_state


if __name__ == "__main__":
    delay = 2
    testing = True
    small_blind = 5
    wager = 200
    wallet = 2000
    # print("Press 's' to start playing.")
    # keyboard.wait('s')
    play = Game(delay, small_blind, wager, wallet, testing)

    # play.hand = ['4s', 'Kd']
    # play.opp_pushed = False
    # play.player_action()
    play.run()
