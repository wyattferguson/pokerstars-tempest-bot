
import holdem_functions
import holdem_argparser


class Holdem():
    def __init__(self, board: list[str] = None, exact: bool = False, simulations: int = 100000,
                 hole_cards: list[str] = None, verbose: bool = False) -> None:
        self.input_file = None
        self.verbose = verbose
        args = holdem_argparser.LibArgs(board, exact, simulations, self.input_file, hole_cards)
        self.hole_cards, self.simulations, self.exact, self.board, filename = holdem_argparser.parse_lib_args(args)

        self.deck = holdem_functions.generate_deck(self.hole_cards, self.board)

    def simulate(self):
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

        # Choose whether we're running a Monte Carlo or exhaustive simulation
        board_length = 0 if self.board is None else len(self.board)
        # When a board is given, exact calculation is much faster than Monte Carlo
        # simulation, so default to exact if a board is given
        if self.exact or self.board is not None:
            generate_boards = holdem_functions.generate_exhaustive_boards
        else:
            generate_boards = holdem_functions.generate_random_boards

        if (None, None) in self.hole_cards:
            hole_cards_list = list(self.hole_cards)
            unknown_index = self.hole_cards.index((None, None))
            for filler_hole_cards in holdem_functions.generate_hole_cards(self.deck):
                hole_cards_list[unknown_index] = filler_hole_cards
                deck_list = list(self.deck)
                deck_list.remove(filler_hole_cards[0])
                deck_list.remove(filler_hole_cards[1])
                holdem_functions.find_winner(generate_boards, tuple(deck_list),
                                             tuple(hole_cards_list), self.simulations,
                                             board_length, self.board, winner_list,
                                             result_histograms)
        else:
            holdem_functions.find_winner(generate_boards, self.deck, self.hole_cards, self.simulations,
                                         board_length, self.board, winner_list,
                                         result_histograms)
        if self.verbose:
            holdem_functions.print_results(self.hole_cards, winner_list,
                                           result_histograms)
        return holdem_functions.find_winning_percentage(winner_list)
