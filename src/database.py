import sqlite3
from sqlite3 import Error
from typing import Any

from _config import DIR_PATH, MAX_STACK
from _types import Action, Card


class DB:
    """simple sqllite3 wrapper."""

    def __init__(self) -> None:
        self.db_name = "../pushfold.db"
        try:
            db_path = DIR_PATH / self.db_name
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = self.dict_factory
            self.cur = self.conn.cursor()
        except Error as e:
            raise RuntimeError(f"Could not connect to Database: {e}")

    def dict_factory(self, cursor, row: dict) -> dict:
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def hand(self, hand: list[Card]) -> dict:
        qry = "SELECT * FROM hands \
            WHERE (card1 = ? AND card2 = ?) \
            OR (card1 = ? AND card2 = ?) \
            LIMIT 1"
        return self._run(qry, (str(hand[0]), str(hand[1]), str(hand[1]), str(hand[0])))

    def nash(self, stack: float, opp_pushed: bool, hand: list[Card]) -> dict:
        # keep stack within bounds (1.1 -> 200)
        if stack <= 1:
            stack = 1.1
        elif stack > MAX_STACK:
            stack = MAX_STACK

        status = Action.CALL if opp_pushed else Action.PUSH

        # nash name could be in 2 different formats so try both if needed
        try:
            row = self._nash_lookup(hand[0], hand[1], status, stack)
        except Exception:
            row = self._nash_lookup(hand[1], hand[0], status, stack)

        return row

    def _nash_lookup(self, h1: Card, h2: Card, status: str, stack: float) -> str:
        name = f"{h1.value}{h2.value}"
        if h1.value != h2.value:
            suited = "s" if h1.suit == h2.suit else "o"
            name = f"{name}{suited}"

        qry = "SELECT id, status, stack, x? as score FROM nash \
            WHERE status = ? AND stack = ? \
            LIMIT 1"
        return self._run(qry, (name.strip(), status, stack))

    def _run(self, qry: str = "", params: tuple = None) -> dict[str, Any]:
        run = self.cur.execute(qry, params or ())
        return run.fetchone()
