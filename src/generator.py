from config import *
from montecarlo import MonteCarlo
import treys
import eval7
import pandas as pd


class Generator():
    def __init__(self, test: bool = True, verbose: bool = False,
                 board: list[str] = [], interations: int = 1000) -> None:
        self.db = DB()
        self.test = test
        self.verbose = verbose
        self.board = board
        self.interations = interations

    def run(self, model: str = False) -> None:
        start = time.time()
        if model == "monte":
            gen_model = self.monte_pairs
        elif model == "rank":
            gen_model = self.hand_rank
        elif model == "eval7":
            gen_model = self.eval_seven
        else:
            print("#### Error: Invalid Model Given ####")
            exit()

        sub_deck = DECK.copy()
        for card1 in DECK:
            sub_deck.pop(0)
            for card2 in sub_deck:
                gen_model(card1, card2)

        print("Time elapsed(seconds): ", round(time.time() - start, 3))

    def get_random_hand(self, size: int = 2) -> list:
        return random.sample(DECK, size)

    def get_random_board(self, board_size: int = 3) -> list:
        return self.get_random_hand(board_size)

    def import_nash_tables(self) -> None:
        # create all the coloumn names from the csv
        for status in ["call", "push"]:
            nash_data = pd.read_csv(f"{DIR_PATH}\\data\\nash_{status}.csv", header=0, squeeze=True).to_dict()

            for key, value in nash_data.items():
                col = "x" + key.strip()
                self.db.add_table_column("nash", col, "REAL")

        # write all data from call / push csv
        for status in ["call", "push"]:
            nash_data = pd.read_csv(f"{DIR_PATH}\\data\\nash_{status}.csv", header=0, squeeze=True).to_dict()
            cnt = 0
            while True:
                row = {'status': status}
                for key, value in nash_data.items():
                    col = 'x' + key.strip()
                    row[col] = value[cnt]
                if cnt > 0:
                    self.db.insert("nash", row)
                cnt += 1

    def eval_seven(self, card1: str = "", card2: str = "") -> None:
        hand = [eval7.Card(card1), eval7.Card(card2)]

        score = eval7.evaluate(hand)
        if self.verbose:
            print(card1, card2, score)

        if not self.test:
            self.db.update_hand_score(card1, card2, score)

    def hand_rank(self, card1: str = "", card2: str = "") -> None:
        hand = [
            treys.Card.new(card1),
            treys.Card.new(card2)
        ]

        evaluator = treys.Evaluator()

        sub_deck1 = DECK.copy()
        for c1 in DECK:
            sub_deck1.pop(0)
            sub_deck2 = sub_deck1.copy()
            for c2 in sub_deck1:
                sub_deck2.pop(0)
                for c3 in sub_deck2:
                    if not bool(set([c1, c2, c3]) & set([card1, card2])):
                        board = [
                            treys.Card.new(c1),
                            treys.Card.new(c2),
                            treys.Card.new(c3)
                        ]

                        hand_score = evaluator.evaluate(board, hand)
                        hand_class = evaluator.get_rank_class(hand_score)

                        if self.verbose:
                            print(f"({card1} {card2} | {c1}{c2}{c3}) {hand_score} ({evaluator.class_to_string(hand_class)})")

                        if not self.test:
                            row = {
                                "card1": card1,
                                "card2": card2,
                                "board": f"{c1}{c2}{c3}",
                                "rank": hand_score,
                                "class": hand_class
                            }

                            self.db.insert("hand_ranks", row)

    def monte_pairs(self, card1: str = "", card2: str = "") -> None:
        # board = ["As", "Ks", "Jd"]
        exact_precision = False

        hand = [card1, card2] + ["?", "?"]
        monte = MonteCarlo(self.board, exact_precision, self.interations, hand, self.verbose)

        #   Tie, Win, Loss
        #  [0.08, 0.48, 0.43]
        results = monte.simulate()

        if self.verbose:
            print(card1, card2, results)

        if not self.test:
            row = {
                "card1": card1,
                "card2": card2,
                "win": results[1],
                "tie": results[0],
                "loss": results[2],
            }

            self.db.insert("hands", row)


if __name__ == "__main__":
    gen = Generator(test=True, verbose=True)
    # print(gen.get_random_hand())
    # print(gen.run(model="monte"))
    # print(gen.run(model="rank"))
    # print(gen.run(model="eval7"))
    gen.import_nash_tables()
    # gen.eval_seven()
