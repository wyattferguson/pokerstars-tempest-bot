
import keyboard
from pyautogui import hotkey
from config import *
from database import DB
from vision import Vision


class Game():
    """ Tempest Game Simulator """

    def __init__(self, small_blind: int = 1, wallet: int = 50, wager: int = 0) -> None:
        self.delay = 1
        self.pot = 0
        self.hand = []
        self.hand_odds = 0
        self.games = 0
        self.live = LIVE_PLAY
        self.use_keys = USE_KEYS
        self.testing = TESTING
        self.wager = wager
        self.stacks = 0
        self.sb = small_blind
        self.bb = 2 * self.sb
        self.opp_pushed = False
        self.wallet = wallet
        self.action = False
        self.vsn = Vision()
        self.db = DB()

    def run(self) -> None:
        """ Main game loop """

        print("Runnning!")
        while True:

            new_hand = self.vsn.cards()
            if new_hand and new_hand != self.hand and len(new_hand) == 2:
                self.log(f"New Hand -> {new_hand}")

                tmp_wallet = self.vsn.read_wallet()
                if tmp_wallet and tmp_wallet > 0:
                    self.wallet = tmp_wallet

                self.hand = new_hand
                self.games += 1

                winp = self.db.get_hand(self.hand)
                self.hand_odds = round(winp['win'], 2)
                self.log(f"Odds -> {self.hand_odds * 100}")

                self.wait_for_turn()

                self.pot = self.vsn.read_pot()
                self.log(f"Pot -> {self.pot}")

                self.opp_pushed = True if self.pot > self.sb + self.bb else False
                self.log(f"Opp Pushed -> {self.opp_pushed }")

                if self.wager > 0:
                    self.strategy()
                else:
                    self.action = "No Wager"

                self.print_summary()

            time.sleep(self.delay)

    def wait_for_turn(self) -> None:
        # wait until your timer appears
        self.log("Waiting for my Turn")
        if not self.testing or self.live:
            while not self.vsn.read_timer():
                time.sleep(self.delay)

    def random_delay(self) -> None:
        """ Delay game actions for a random amount of time """

        delay = round(random.uniform(DELAY_LOWER, DELAY_UPPER), 1)
        self.log(f"Delay -> {delay}s")
        if not self.testing:
            time.sleep(delay)

    def fold(self) -> None:
        """ fold dealt hand """

        self.action = "fold"
        self.log("Action -> Folding")
        if self.use_keys:
            hotkey('ctrl', 'alt', 'f')

    def push_allin(self) -> None:
        """ Push hand in """

        self.action = "call"
        self.log("Action -> Calling")
        if self.use_keys:
            hotkey('ctrl', 'alt', 'c')

    def strategy(self) -> None:
        """ Nash push/fold strategy """

        self.stacks = round(self.wager / self.bb, 1)
        status = "call" if self.opp_pushed else "push"
        nash_row = self.db.get_nash(self.stacks, status, self.hand)

        if not self.testing:
            self.random_delay()

        self.log(nash_row)

        if nash_row['score'] >= 0.5:
            self.push_allin()
        else:
            self.fold()

    def log(self, message: any) -> None:
        """ Print message to console for testing debug """

        if self.testing:
            print(message)

    def print_summary(self) -> None:
        """ Print current game details to console """

        print("\n###### SUMMARY ######\n")
        print(f"Game: {self.games}")
        print(f"Pot: {self.pot}")
        print(f"Purse: {self.wager} \\ {self.wallet} ({self.stacks} Stacks)")
        print(f"Hand: {self.hand} ({self.hand_odds}%)")
        print(f"Opponent Pushed: {self.opp_pushed}")
        print(f"Action: {self.action}")
        print("\n####################\n")


if __name__ == "__main__":
    small_blind = 0.50
    wallet = 10  # buy in amount
    wager = 1
    if not TESTING:
        print("Press 's' to start playing.")
        keyboard.wait('s')

    play = Game(small_blind, wallet, wager)
    play.run()
