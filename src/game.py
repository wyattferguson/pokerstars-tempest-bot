
import keyboard
from pyautogui import hotkey
import logging

from config import *
from vision import Vision


class Game():
    def __init__(self, delay: int = 1, small_blind: int = 500, base_wager: int = 0,
                 wallet: int = 200000, testing: bool = True) -> None:
        self.delay = delay
        self.players = 0
        self.pot = 0
        self.hand = []
        self.hand_odds = 0
        self.games = 0
        self.testing = testing
        self.wager = 0
        self.stacks = 0
        self.base_wager = base_wager
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
        print("Runnning!")
        while True:
            self.wallet, self.wager = self.vsn.read_wallet(self.wallet, self.wager)
            new_hand = self.vsn.cards()
            if new_hand and new_hand != self.hand and len(new_hand) == 2:
                print("Wager -> ", self.wager)
                print(f"New Hand -> {new_hand}")

                self.hand = new_hand
                self.games += 1

                if not self.testing:
                    while not self.vsn.read_timer():
                        time.sleep(1)

                self.pot = self.vsn.read_pot()
                print("Pot -> ", self.pot)

                self.opp_pushed, self.players = self.vsn.read_players()
                if self.wager > 0:
                    self.strategy()
                else:
                    self.action = "No Wager"
                self.print_status()
            # else:

            #     print("Waiting for hand...")
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
            hotkey('ctrl', 'alt', 'f')

    def push_allin(self) -> None:
        self.action = "call"
        print("Action -> Calling")
        if not self.testing:
            hotkey('ctrl', 'alt', 'c')

    def strategy(self) -> None:
        self.stacks = round(self.wager / self.gb, 1)
        status = "call" if self.opp_pushed else "push"
        nash_row = self.db.get_nash(self.stacks, status, self.hand)

        winp = self.db.get_hand(self.hand)
        self.hand_odds = round(winp['win'], 2)
        if not self.testing:
            self.random_delay()

        print(nash_row)
        if nash_row['score'] >= 0.5:
            self.push_allin()
        else:
            self.fold()

    def print_status(self):
        print("\n###### SUMMARY ######\n")
        print(f"Game: {self.games}")
        print(f"Pot: {self.pot}")
        print(f"Purse: {self.wager} \\ {self.wallet} ({self.stacks} Stacks)")
        print(f"Hand: {self.hand} ({self.hand_odds}%)")
        print(f"Opponent Pushed: {self.opp_pushed}")
        print(f"Action: {self.action}")
        print("\n####################\n")

    def __str__(self) -> str:
        game_state = f"POT: {self.pot} | PLYS: {self.players} | WLT: {self.wallet} | WGR: {self.wager} | GMS: {self.games} | HND: {self.hand} | OPP: {self.opp_pushed} | ACT: {self.action}"
        if not self.testing:
            self.logger.info(game_state)
        return game_state


if __name__ == "__main__":
    delay = 2
    testing = True
    base_wager = 20000
    small_blind = 500
    wallet = 100000
    # print("Press 's' to start playing.")
    # keyboard.wait('s')
    play = Game(delay, small_blind, base_wager, wallet, testing)

    # play.hand = ['4s', 'Kd']
    # play.opp_pushed = False
    # play.player_action()
    play.run()
