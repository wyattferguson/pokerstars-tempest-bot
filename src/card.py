
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
    pass
