from dataclasses import dataclass, field
from enum import StrEnum


@dataclass(frozen=True)
class Card:
    value: str = field(init=True)
    suit: str = field(init=True)

    def __repr__(self) -> str:
        return f"{self.value}{self.suit}"


class Action(StrEnum):
    WAIT = "wait"
    CALL = "call"
    FOLD = "fold"
    PUSH = "push"


@dataclass
class Location:
    x: int = field(init=True)
    y: int = field(init=True)
    width: int = field(init=True)
    height: int = field(init=True)

    def __post_init__(self) -> None:
        if self.x < 0:
            raise ValueError(f"Invalid X Coordinate: {self.x}")
        if self.y < 0:
            raise ValueError(f"Invalid Y Coordinate: {self.y}")
        if self.width <= 0:
            raise ValueError(f"Invalid Width: {self.width}")
        if self.height <= 0:
            raise ValueError(f"Invalid Height: {self.height}")

    @property
    def pos(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)
