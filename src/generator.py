from config import *
from montecarlo_model import MonteCarlo
from database import DB

db = DB()


def monte_pairs():
    start = time.time()
    # board = ["As", "Ks", "Jd"]
    board = None
    exact_precision = False
    interations = 1000
    verbose = False

    sub_deck = DECK.copy()

    for c1 in DECK:
        sub_deck.pop(0)
        for c2 in sub_deck:
            hand = [c1, c2] + ["?", "?"]
            model = MonteCarlo(board, exact_precision, interations, hand, verbose)
            #   Tie, Win, Loss
            #  [0.08, 0.48, 0.43]
            results = model.simulate()
            print(c1, c2, results)

            row = {
                "card1": c1,
                "card2": c2,
                "win": results[1],
                "tie": results[0],
                "loss": results[2],
            }
            db.insert("hands", row)

    print("Time elapsed(seconds): ", round(time.time() - start, 3))


if __name__ == "__main__":
    monte_pairs()
