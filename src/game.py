
import keyboard
from pyautogui import hotkey
from config import *
from database import DB
from card import Card
from vision import Vision


class Game():
    def __init__(self, delay: int = 1, small_blind: int = 500,
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
        self.sb = small_blind
        self.bb = 2 * self.sb
        self.gb = 2 * self.bb
        self.opp_pushed = False
        self.wallet = wallet
        self.action = False
        self.vsn = Vision()
        self.db = DB()

    def run(self) -> None:
        print("Runnning!")
        while True:
            self.wallet, self.wager = self.vsn.read_wallet(self.wallet, self.wager)
            new_hand = self.vsn.cards()
            if new_hand and new_hand != self.hand and len(new_hand) == 2:
                self.log(f"Wager -> {self.wager}")
                self.log(f"New Hand -> {new_hand}")

                self.hand = new_hand
                self.games += 1

                # wait until your timer appears
                if not self.testing:
                    while not self.vsn.read_timer():
                        time.sleep(1)

                self.pot = self.vsn.read_pot()
                self.log("Pot -> ", self.pot)

                self.opp_pushed, self.players = self.vsn.read_players()
                self.log(f"Players -> {self.players }")
                if self.wager > 0:
                    self.strategy()
                else:
                    self.action = "No Wager"

                self.print_summary()

            time.sleep(self.delay)

    def random_delay(self) -> None:
        delay = round(random.uniform(DELAY_LOWER, DELAY_UPPER), 1)
        self.log(f"Delay -> {delay}s")
        if not self.testing:
            time.sleep(delay)

    def fold(self) -> None:
        self.action = "fold"
        self.log("Action -> Folding")
        if not self.testing:
            hotkey('ctrl', 'alt', 'f')

    def push_allin(self) -> None:
        self.action = "call"
        self.log("Action -> Calling")
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

        self.log(nash_row)
        if nash_row['score'] >= 0.5:
            self.push_allin()
        else:
            self.fold()

    def log(self, message: any) -> None:
        if testing:
            print(message)

    def print_summary(self) -> None:
        print("\n###### SUMMARY ######\n")
        print(f"Game: {self.games}")
        print(f"Pot: {self.pot}")
        print(f"Purse: {self.wager} \\ {self.wallet} ({self.stacks} Stacks)")
        print(f"Hand: {self.hand} ({self.hand_odds}%)")
        print(f"Opponent Pushed: {self.opp_pushed}")
        print(f"Action: {self.action}")
        print("\n####################\n")


if __name__ == "__main__":
    delay = 2
    testing = True
    small_blind = 500
    wallet = 100000
    if not testing:
        print("Press 's' to start playing.")
        keyboard.wait('s')
    play = Game(delay, small_blind, wallet, testing)
    play.run()
