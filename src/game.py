
import time

from pyautogui import hotkey

from config import ACTIONS, HAND_WAGER, SMALL_BLIND, TESTING, USE_KEYS
from database import DB
from vision import Vision


class Game():
    """ PokerStars Tempest Game Player """

    def __init__(self) -> None:
        self.delay = 1  # Delay between new hand check in seconds
        self.pot = 0
        self.hand = []
        self.hand_odds = 0
        self.base_wager = HAND_WAGER
        self.wager = HAND_WAGER
        self.stacks = 0
        self.sb = SMALL_BLIND
        self.bb = 2 * self.sb  # big blind
        self.gb = 2 * self.bb  # giant blind
        self.pot_min = self.sb + self.bb + self.gb
        self.opp_pushed = False  # has another player pushed all in
        self.action = False
        self.vsn = Vision()
        self.db = DB()

    def run(self) -> None:
        """ Main game loop """

        print("Runnning!")
        while True:
            new_hand = self.vsn.cards()
            self.update_wager()
            if new_hand and new_hand != self.hand and len(new_hand) == 2:
                self.hand = new_hand
                hand_info = self.db.hand(self.hand)
                self.hand_odds = round(hand_info['win'], 2) * 100
                self.wait_for_turn()
                self.pot = self.vsn.read_pot()
                self.opp_pushed = True if self.pot > self.pot_min else False
                self.strategy()

                print(self)

            time.sleep(self.delay)

    def wait_for_turn(self) -> None:
        """ wait for your timer to appear """
        if not TESTING:
            while not self.vsn.read_timer():
                time.sleep(self.delay)

    def update_wager(self):
        """ Try to read hand wager """
        try:
            tmp_wager = self.vsn.read_wallet()
            if tmp_wager and float(tmp_wager) != self.wager:
                self.wager = float(tmp_wager)
        except Exception:
            self.wager = self.base_wager

    def strategy(self) -> None:
        """ Nash push/fold strategy """
        if self.wager > 0:
            self.stacks = round(self.wager / self.gb, 1)
            nash_row = self.db.nash(self.stacks, self.opp_pushed, self.hand)

            self.action = 'call' if nash_row['score'] >= 0.5 else 'fold'
            if USE_KEYS:
                hotkey(*ACTIONS[self.action])
        else:
            self.action = "No wager"

    def __str__(self) -> str:
        return f"""
        ###### SUMMARY ######
        Pot: {self.pot}
        Purse: {self.wager} ({self.stacks} Stacks)
        Hand: {self.hand} ({self.hand_odds}%)
        Opponent Pushed: {self.opp_pushed}
        Action: {self.action}
        """


if __name__ == "__main__":
    play = Game()
    play.run()
