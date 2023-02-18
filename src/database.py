import sqlite3
from sqlite3 import Error

from config import *
from card import Card

DATABASE = "../madrid.db"


class DB:
    """
    Generic sqlLite3 library
    """

    def __init__(self, test: bool = False) -> None:
        self.test = test
        try:
            db_path = DIR_PATH / DATABASE
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = self.dict_factory
            self.cur = self.conn.cursor()
        except Error as e:
            raise RuntimeError(f"Could not connect to Database: {e}")

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def update(self, table: str = "hands", data: dict = {}, id_field: str = "id", id_value: any = 0) -> bool:
        """
        Generic update function

        Args:
            table (str): Table name. Defaults to "matches".
            data (dict): Dictionary of values.
            id_field (int): Id field name. Defaults to "id".
            id_value (int): Id value.
        """
        values = ""
        for key, val in data.items():
            values += f"{key} = "
            values += f"{val}," if isinstance(val, int) else f"'{val}',"

        where = f"{id_field} = "
        where += f"{id_value}" if isinstance(id_value,
                                             int) else f"'{id_value}'"
        qry = f"UPDATE {table} SET {values[:-1]} WHERE {where}"
        self.cur.execute(qry)
        self.conn.commit()
        return True if self.cur.rowcount > 0 else False

    def insert(self, table: str, values: dict) -> None:
        """
        Generic insert, serializes values for insertion

        Args:
            table (str): Table name.
            values (dict): Dictionary of key->value data
        """
        keys = '","'.join(values.keys())
        marks = ','.join(list('?' * len(values)))
        values = tuple(values.values())
        self.conn.execute('INSERT INTO ' + table +
                          ' ("' + keys + '") VALUES (' + marks + ')', values)
        self.conn.commit()

    def match_exists(self, name: str, game_id: str, role: str = "player") -> bool:
        """
        Check if game already exists in player_matches

        Args:
            player (str): Player name
            game_id (str): Oracle Game ID

        Returns:
            bool: True game exisists, False game hasnt been recored yet.
        """
        qry = f"SELECT COUNT(*) FROM {role}_matches WHERE {role} = '{name}' AND game_id = '{game_id}'"
        cnt = self.conn.execute(qry)
        return True if cnt.fetchone()[0] else False

    def get_by_game_id(self, table: str, game_id: str, team: str, return_single: bool = False) -> list:
        """Get rows by game_id and team name"""
        qry = f"SELECT * FROM {table} WHERE game_id = '{game_id}' AND team = '{team}'"
        return self._run(qry, return_single)

    def get_features(self, min_val: int = 0, role: str = "team"):
        """Get features for model training

        Args:
            min_val (int): Minimum abs value of the slope for a feature
        """

        qry = f"SELECT * FROM features WHERE abs_val > {min_val} AND role = '{role}' ORDER BY abs_val ASC"
        return self._run(qry, False)

    def distinct(self, table: str, select: str, where_field: str = False,
                 where_value: str = False, order_by: str = False, direction: str = False) -> list:
        """Get only unique results for a given field"""
        if not table:
            raise ValueError("Table name not provided.")

        if not select:
            raise ValueError("Select field must be included.")

        qry = f"SELECT DISTINCT {select} FROM {table} "
        if where_field:
            qry += f"WHERE {where_field} = '{where_value}' "
        if order_by and direction:
            qry += f"ORDER BY {order_by} {direction}"

        return self._run(qry, False)

    def get(self, table: str, where_field: str = False, where_value: str = False,
            order_by: str = False, direction: str = False) -> list:
        """
        Generic get from table

        Args:
            table (str): Table name
            where_field (str, optional): Field to select against. Defaults to False.
            where_value (str, optional): Value to match. Defaults to False.
            order_by (str, optional): Field to order by. Defaults to False.
            direction (str, optional): Direction to sort by. Defaults to False.

        Returns:
            list: fetch all results
        """
        if not table:
            raise ValueError("Table name not provided.")

        qry = f"SELECT * FROM {table} "
        if where_field:
            qry += f"WHERE {where_field} = '{where_value}' "
        if order_by and direction:
            qry += f"ORDER BY {order_by} {direction}"

        return self._run(qry, False)

    def get_hand(self, hand: list[str]):
        qry = f"SELECT * FROM hands WHERE (card1 = '{hand[0]}' AND card2 = '{hand[1]}') OR (card1 = '{hand[1]}' AND card2 = '{hand[0]}') LIMIT 1"
        if self.test:
            print(qry)
        return self._run(qry)

    def get_nash(self, stack: float, status: str, hand: list[str]):
        row_name = self.nash_name(hand[0], hand[1])
        if stack < 1:
            stack = 1.1
        elif stack > 200:
            stack = 200

        try:
            qry = f"SELECT id, status, stack, x{row_name.strip()} as score FROM nash WHERE status = '{status}' AND stack = '{stack}' LIMIT 1"
            run = self.cur.execute(qry)
        except Exception as e:
            row_name = self.nash_name(hand[1], hand[0])
            qry = f"SELECT id, status, stack, x{row_name.strip()} as score FROM nash WHERE status = '{status}' AND stack = '{stack}' LIMIT 1"
            run = self.cur.execute(qry)
        if self.test:
            print(qry)
        return run.fetchone()

    def nash_name(self, h1: str, h2: str) -> str:
        name = ""
        if h1.value == h2.value:
            name = f"{h1.value}{h2.value}"
        else:
            suited = "s" if h1.suit == h2.suit else "o"
            name = f"{h1.value}{h2.value}{suited}"
        return name

    def get_single(self, table: str, where_field: str = False, where_value: str = False) -> dict:
        """
        Get a single row from given tabe

        Args:
            table (str): Table name
            where_field (str, optional): Field to select against. Defaults to False.
            where_value (str, optional): Value to match. Defaults to False.

        Returns:
            dict: Single table row
        """
        if not table:
            raise ValueError("Table name not provided.")

        qry = f"SELECT * FROM {table} "
        if where_field:
            qry += f"WHERE {where_field} = '{where_value}' "

        qry += " LIMIT 1"
        return self._run(qry)

    def update_hand_score(self, card1: str, card2: str, score: int) -> bool:
        qry = f"UPDATE hands SET score = {score} WHERE card1 = '{card1}' AND card2 = '{card2}'"
        self.cur.execute(qry)
        self.conn.commit()
        return True if self.cur.rowcount > 0 else False

    def clear_table(self, table: str) -> None:
        """
        Empty all rows from a given table

        Args:
            table (str): Table name
        """
        self.delete(table, 1, 1)
        self.conn.commit()

    def add_table_column(self, table_name: str, col_name: str, col_type: str = 'float'):
        self.cur.execute(
            f"ALTER TABLE {table_name} ADD COLUMN '{col_name}' '{col_type}'")
        self.conn.commit()

    def create_table_from_list(self, table_name: str, col_names: list):
        """Create all the coloumns from a given list in a new table"""
        cols = " FLOAT, ".join(col_names)
        qry = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols} float)"
        # print(qry)
        run = self.cur.execute(qry)
        self.conn.commit()

    def delete(self, table: str, id_field: str = "id", id: int = 0) -> None:
        """
        Generic delete from table

        Args:
            table (str): Table name
            id_field (str): Table id_field to match id. Defaults to "id".
            id (int): Row Id value
        """

        if not table:
            raise ValueError("Table name not provided.")

        self.conn.execute(f"DELETE FROM {table} WHERE {id_field} = {id}")
        self.conn.commit()

    def _run(self, qry: str, single: bool = True):
        run = self.cur.execute(qry)
        return run.fetchone() if single else run.fetchall()


if __name__ == "__main__":
    pass
