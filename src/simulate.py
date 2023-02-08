
from config import *
from card import Card
import holdem_functions


class Simulate():
    def __init__(self, board: list[str] = None, exact: bool = False, simulations: int = 100000,
                 hole_cards: list[str] = None, verbose: bool = False) -> None:
        self.board = self.create_cards(board) if board else None
        self.exact = exact
        self.simulations = simulations
        self.hole_cards = self.create_cards(hole_cards) if hole_cards else None
        self.verbose = verbose
        print(self.hole_cards)

    def create_cards(self, cards):
        print(cards)
        return [Card(card) for card in cards]

    def calculate(self):
        deck = holdem_functions.generate_deck(self.hole_cards, self.board)
        num_players = len(self.hole_cards)

        # Create results data structures which track results of comparisons
        # 1) result_histograms: a list for each player that shows the number of
        #    times each type of poker hand (e.g. flush, straight) was gotten
        # 2) winner_list: number of times each player wins the given round
        # 3) result_list: list of the best possible poker hand for each pair of
        #    hole cards for a given board
        result_histograms, winner_list = [], [0] * (num_players + 1)
        for _ in range(num_players):
            result_histograms.append([0] * len(holdem_functions.HAND_RANKINGS))

        # When a board is given, exact calculation is much faster than Monte Carlo
        # simulation, so default to exact if a board is given
        if self.exact or self.board is not None:
            generate_boards = holdem_functions.generate_exhaustive_boards
        else:
            generate_boards = holdem_functions.generate_random_boards

        holdem_functions.find_winner(generate_boards, deck, self.hole_cards, self.simulations,
                                     self.board, winner_list,
                                     result_histograms)
        if self.verbose:
            holdem_functions.print_results(self.hole_cards, winner_list, result_histograms)

        return holdem_functions.find_winning_percentage(winner_list)
