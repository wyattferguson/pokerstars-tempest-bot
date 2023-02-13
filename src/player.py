'''
TODO:
- Fix Nash stack calculation
- Add proper decision tree for nash
- Add MonteCarlo look up + Decision tree

'''
from config import *


class Player():
    def __init__(self, player_name: str = "", max_bet: int = 200, wallet: int = 10000) -> None:
        self.start_wallet = wallet
        self.wallet = wallet
        self.player_name = player_name
        self.playing = True
        self.status = "waiting"
        self.max_bet = max_bet
        self.bet = 0
        self.blind = 0
        self.is_small_blind = False
        self.hand = []
        self.wins = 0
        self.buy_ins = 1
        self.total_games = 0
        self.total_hands = 0
        self.folds = 0
        self.db = DB()

    def new_hand(self, hand: list, blind: int = 0, is_small_blind: bool = False):
        self.status = "new hand"
        self.is_small_blind = is_small_blind
        self.bet = self.max_bet if self.wallet > self.max_bet else self.wallet
        self.hand = hand
        self.blind = blind
        self.wallet -= self.blind
        self.bet = 0
        self.total_games += 1
        print(self)

    def is_playing(self) -> bool:
        if self.wallet <= 0 and self.playing:
            self.status = "broke"
            self.playing = False

        return self.playing

    def win(self, pot: int = 0):
        self.status = "winner"
        self.wins += 1
        self.blind = 0
        self.bet = 0
        print(f"{self} | +{pot} | {self.wallet + pot}")
        self.wallet += pot

    def push(self) -> int:
        self.playing = True
        self.status = "push"
        self.total_hands += 1
        self.bet = self.max_bet - self.blind
        self.wallet -= self.bet
        return self.bet

    def fold(self) -> int:
        self.status = "fold"
        self.folds += 1
        self.playing = False
        return 0

    def stats(self) -> None:
        print(f"\n########## Player {self.player_name} Stats ##########")
        print(f"Total Games: {self.total_games}")
        print(
            f"Stats(W/L/F/H): {self.wins} / {self.total_hands - self.wins} / {self.folds} / {self.total_hands}")
        wp = round(self.wins / self.total_hands, 4) * 100
        lp = 100 - wp
        hp = round(self.total_hands / self.total_games, 4) * 100
        print(f"Stats % (W/L/T/H): {wp} / {lp} / {hp}")
        print(f"Wallet: {self.wallet}")
        print(f"Buy Ins: {self.buy_ins}")
        profit = self.start_wallet - self.wallet
        print(f"Profit: {profit}")
        pph = round(profit / self.total_hands, 4)
        print(f"Pofit Per Hand: {pph}")

    def __str__(self) -> str:
        return (f"{self.player_name} -> {self.status} | {self.hand} ({self.bet} | {self.blind} | {round(self.wallet,2)})")


class Chaos(Player):
    """ Random Push/Fold """

    def __init__(self, player_name: str = "Chaos"):
        super().__init__("C-" + player_name)

    def move(self, call: bool = False) -> int:
        return self.push() if bool(random.getrandbits(1)) else self.fold()


class Nash(Player):
    """ Nash Tables """

    def __init__(self, player_name: str = "Nash", max_bet: int = 200, wallet: int = 10000):
        super().__init__("N-" + player_name, max_bet, wallet)

    def move(self, call: bool = False) -> int:
        status = 'call' if call else 'push'

        if not isinstance(self.hand, list):
            hand = []
            for c in self.hand:
                hand.append(str(FACE_CARDS.get(c.rank, c.rank)) + c.suit)
        else:
            hand = self.hand

        # FIX THIS
        stack = 1.0

        self.db.get_nash(stack, status, hand)
        return self.push() if bool(random.getrandbits(1)) else self.fold()


class Monte(Player):
    """ MonteCarlo Hand Percentages """

    def __init__(self, player_name: str = "Monte", min_push_score: float = 40):
        self.min_push_score = min_push_score
        super().__init__("M-" + player_name)

    def move(self, call: bool = False):
        pass


if __name__ == "__main__":
    db = DB()
    hand = ['3c', '2h']
    status = "call"
    stack = 1.15
    row = db.get_nash(stack, status, hand)
    print(row)
