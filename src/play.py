from config import *
from simulate import Simulate


def run():
    #print(holdem_calc.calculate(["As", "Ks", "Jd"], True, 1, None, ["8s", "7s", "Qc", "Th"], False))
    pass


if __name__ == "__main__":
    poker = Simulate(["As", "Ks", "Jd"], True, 10000, ["8s", "7s", "Qc", "Th"])
    print(poker.calculate())
