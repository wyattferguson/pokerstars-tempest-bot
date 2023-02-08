from config import *
import holdem_calc


def run():
    #print(holdem_calc.calculate(["As", "Ks", "Jd"], True, 1, None, ["8s", "7s", "Qc", "Th"], False))
    pass


if __name__ == "__main__":
    #board = ["As", "Ks", "Jd"]
    board = None
    exact_precision = False
    interations = 10000
    hand = ["8s", "7s", "?", "?"]
    verbose = True

    #   Tie, Win, Loss
    #  [0.08, 0.48, 0.43]
    print(holdem_calc.calculate(board, exact_precision, interations, hand, verbose))
