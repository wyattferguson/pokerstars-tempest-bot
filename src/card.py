
from dataclasses import dataclass, field
from config import ALL_CARDS, SUITS


@dataclass
class Card:
    value: str = field(init=True)
    suit: str = field(init=True)

    def __post_init__(self):
        if self.value not in ALL_CARDS:
            raise ValueError(f"Invalid Card Value: {self.value}")

        if self.suit not in SUITS:
            raise ValueError(f"Invalid Suit: {self.suit}")

    def __repr__(self) -> str:
        return f"{self.value}{self.suit}"


if __name__ == "__main__":
    pass
    # hand = [Card("9", "c"), Card("2", "d")]
    # if Card("9", "c") == Card("9", "c"):
    #     print("THE SAME")
    # else:
    #     print("DIFF")

    # error = Card("L", "s")  # value error

    # error = Card("T", "i")  # suit error
