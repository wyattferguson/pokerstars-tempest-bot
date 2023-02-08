from config import *
from holdem_calc import Holdem
import time


def run():
    # print(holdem_calc.calculate(["As", "Ks", "Jd"], True, 1, None, ["8s", "7s", "Qc", "Th"], False))
    pass


if __name__ == "__main__":
    start = time.time()
    # board = ["As", "Ks", "Jd"]
    board = None
    exact_precision = False
    interations = 5
    hand = ["8s", "7s", "?", "?"]
    verbose = True

    holdem = Holdem(board, exact_precision, interations, hand, verbose)
    #   Tie, Win, Loss
    #  [0.08, 0.48, 0.43]
    print(holdem.simulate())
    print("Time elapsed(seconds): ", round(time.time() - start, 3))
