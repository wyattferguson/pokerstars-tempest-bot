
from dataclasses import dataclass, field
from config import ALL_CARDS, SUITS


@dataclass(frozen=True)
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
    c1 = Card("9", "c")
    c2 = Card("Q", "h")
    # hand = [Card("9", "c"), Card("2", "d")]
    if c1 == c2:
        print("THE SAME")
    else:
        print("DIFF")

    print(c1.value)
    c1.value = "K"
    # error = Card("L", "s")  # value error

    # error = Card("T", "i")  # suit error
