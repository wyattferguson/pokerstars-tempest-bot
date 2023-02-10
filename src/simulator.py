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

    def new_hand(self, hand: list[str], blind: int = 0):
        self.bet = self.max_bet if self.wallet > self.max_bet else self.wallet
        self.wallet -= self.bet
        self.hand = hand
        self.blind = blind

    def is_playing(self) -> bool:
        self.playing = True if self.wallet > 0 else False
        if not self.playing:
            print(f"{self.player_name} is BROKE")
            print(self.__str__())
        return self.playing

    def ante_up(self) -> int:
        self.bet -= self.blind
        return self.blind

    def win(self, pot: int = 0):
        self.wallet += pot

    def push(self) -> int:
        return self.bet

    def fold(self) -> int:
        self.playing = False
        return 0

    def __str__(self) -> str:
        return (f"{self.player_name} | Wallet: {self.wallet} | Hands: {self.hands_played} | W: {self.wins} L: {self.losses} T: {self.ties}")


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


class Tempest():
    def __init__(self, players: int = 2) -> None:
        self.num_players = players
        # self.players = [Nash(), Chaos(), Monte()]
        self.players = [Chaos("A1"), Chaos("B2"), Chaos("C3")]
        self.small_blind = 5
        self.big_blind = 2 * self.small_blind
        self.giant_blind = 2 * self.big_blind
        self.blinds = [self.small_blind, self.big_blind, self.giant_blind]
        self.deck = []
        self.pot = 0

    def shuffle_deck(self) -> None:
        self.deck = DECK.copy
        random.shuffle(self.deck)

    def deal(self) -> None:
        self.pot = 0
        self.shuffle_deck()
        for i, p in enumerate(self.players):
            if p.is_playing():
                p.new_hand(self.deal_hand(), self.blinds[i])
                self.pot += p.ante_up()

    def deal_hand(self) -> list[str]:
        return [self.deck.pop(0), self.deck.pop(0)]

    def deal_board(self, cards: int = 5) -> list[str]:
        return self.deck[0:cards]

    def run(self) -> None:
        pass

    def determine_winner(self) -> None:
        pass


if __name__ == "__main__":
    test = Nash("Killer")
    print(test)
