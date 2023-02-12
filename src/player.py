from config import *


class Player():
    def __init__(self, player_name: str) -> None:
        self.wallet = 100000
        self.player_name = player_name
        self.playing = True
        self.max_bet = 200
        self.bet = 0
        self.blind = 0
        self.hand = []
        self.wins = 0
        self.hands_played = 0
        self.ties = 0
        self.losses = 0

    def new_hand(self, hand: list, blind: int = 0):
        self.bet = self.max_bet if self.wallet > self.max_bet else self.wallet
        self.wallet -= self.bet
        self.hand = hand
        self.blind = blind

    def is_playing(self) -> bool:
        self.playing = True if self.wallet > 0 else False
        return self.playing

    def format_cards(self):
        tmp = []
        for c in self.hand:
            tmp.append(str(FACE_CARDS.get(c.rank, c.rank)) + c.suit)
        print(f"{self.player_name} Hand -> {tmp}")
        return tmp

    def ante_up(self) -> int:
        self.bet -= self.blind
        return self.blind

    def win(self, pot: int = 0):
        self.wallet += pot
        print(f"{self.player_name} Wallet -> {round(self.wallet,2)}")

    def push(self) -> int:
        print(f"{self.player_name} Move -> All In ({self.bet})")
        return self.bet

    def fold(self) -> int:
        print(f"{self.player_name} Move -> Fold")
        self.playing = False
        return 0

    def __str__(self) -> str:
        return (f"{self.player_name} | H: {self.hand} | WLT: {self.wallet} | GMS: {self.hands_played} | W: {self.wins} L: {self.losses} T: {self.ties}")


class Chaos(Player):
    """ Random Push/Fold """

    def __init__(self, player_name: str = "Chaos"):
        super().__init__(player_name)

    def move(self) -> int:
        return self.push() if bool(random.getrandbits(1)) else self.fold()


class Nash(Player):
    """ Nash Tables """

    def __init__(self, player_name: str = "Nash"):
        super().__init__(player_name)

    def move(self):
        pass


class Monte(Player):
    """ MonteCarlo Hand Percentages """

    def __init__(self, player_name: str = "Monte"):
        super().__init__(player_name)

    def move(self):
        pass


if __name__ == "__main__":
    db = DB()
    hand = ['3c', '2h']
    status = "call"
    stack = 1.15
    row = db.get_nash(stack, status, hand)
    print(row)
