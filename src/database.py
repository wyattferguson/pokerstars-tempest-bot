import sqlite3
from sqlite3 import Error

from config import *
from card import Card


class DB:
    """ simple sqllite3 wrapper """

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

    def hand(self, hand: list[Card, Card]) -> dict:
        qry = f"SELECT * FROM hands WHERE (card1 = '{hand[0]}' AND card2 = '{hand[1]}') OR (card1 = '{hand[1]}' AND card2 = '{hand[0]}') LIMIT 1"
        return self._run(qry)

    def nash(self, stack: float, opp_pushed: bool, hand: list[Card, Card]) -> dict:
        # keep stack within bounds (1.1 -> 200)
        if stack <= 1:
            stack = 1.1
        elif stack > 200:
            stack = 200

        status = "call" if opp_pushed else "push"

        # nash name could be in 2 different formats so try both if needed
        try:
            row = self._nash_lookup(hand[0], hand[1], status, stack)
        except Exception as e:
            row = self._nash_lookup(hand[1], hand[0], status, stack)

        return row

    def _nash_lookup(self, h1: Card, h2: Card, status: str, stack: float) -> str:
        name = f"{h1.value}{h2.value}"
        if h1.value != h2.value:
            suited = "s" if h1.suit == h2.suit else "o"
            name = f"{name}{suited}"

        qry = f"SELECT id, status, stack, x{name.strip()} as score FROM nash WHERE status = '{status}' AND stack = '{stack}' LIMIT 1"
        return self._run(qry)

    def _run(self, qry: str = "", single: bool = True) -> dict:
        run = self.cur.execute(qry)
        return run.fetchone() if single else run.fetchall()


if __name__ == "__main__":
    pass
