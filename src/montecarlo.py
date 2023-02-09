
import argparse
import re
from config import *


SUITS_INDEX = {"s": 0, "c": 1, "h": 2, "d": 3}

CARDS_STR = "AKQJT98765432"

HAND_RANKINGS = ("High Card", "Pair", "Two Pair", "Three of a Kind",
                 "Straight", "Flush", "Full House", "Four of a Kind",
                 "Straight Flush", "Royal Flush")

CARD_VALUES = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
for card in range(2, 10):
    CARD_VALUES[str(card)] = card


class MonteCarlo():
    def __init__(self, board: list[str] = None, exact: bool = False, simulations: int = 100000,
                 hole_cards: list[str] = None, verbose: bool = False) -> None:
        self.input_file = None
        self.verbose = verbose
        args = LibArgs(board, exact, simulations, self.input_file, hole_cards)
        self.hole_cards, self.simulations, self.exact, self.board, filename = parse_lib_args(args)

        self.deck = generate_deck(self.hole_cards, self.board)

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
            result_histograms.append([0] * len(HAND_RANKINGS))

        # Choose whether we're running a Monte Carlo or exhaustive simulation
        board_length = 0 if self.board is None else len(self.board)
        # When a board is given, exact calculation is much faster than Monte Carlo
        # simulation, so default to exact if a board is given
        if self.exact or self.board is not None:
            generate_boards = generate_exhaustive_boards
        else:
            generate_boards = generate_random_boards

        if (None, None) in self.hole_cards:
            hole_cards_list = list(self.hole_cards)
            unknown_index = self.hole_cards.index((None, None))
            for filler_hole_cards in generate_hole_cards(self.deck):
                hole_cards_list[unknown_index] = filler_hole_cards
                deck_list = list(self.deck)
                deck_list.remove(filler_hole_cards[0])
                deck_list.remove(filler_hole_cards[1])
                find_winner(generate_boards, tuple(deck_list),
                            tuple(hole_cards_list), self.simulations,
                            board_length, self.board, winner_list,
                            result_histograms)
        else:
            find_winner(generate_boards, self.deck, self.hole_cards, self.simulations,
                        board_length, self.board, winner_list,
                        result_histograms)
        if self.verbose:
            print_results(self.hole_cards, winner_list,
                          result_histograms)
        return find_winning_percentage(winner_list)


# Wrapper class which holds the arguments for library calls
# Mocks actual argparse object
class LibArgs:
    def __init__(self, board, exact, num, input_file, hole_cards):
        self.board = board
        self.cards = hole_cards
        self.n = num
        self.input = input_file
        self.exact = exact

# Parses arguments passed to holdem_calc as a library call


def parse_lib_args(args):
    # Parse hole cards and board
    hole_cards, board = None, None
    if not args.input:
        hole_cards, board = parse_cards(args.cards, args.board)
    return hole_cards, args.n, args.exact, board, args.input

# Parses command line arguments to holdem_calc


def parse_args():
    # Define possible command line arguments
    parser = argparse.ArgumentParser(
        description="Find the odds that a Texas Hold'em hand will win. Note "
        "that cards must be given in the following format: As, Jc, Td, 3h.")
    parser.add_argument("cards", nargs="*", type=str, metavar="hole card",
                        help="Hole cards you want to find the odds for.")
    parser.add_argument("-b", "--board", nargs="*", type=str, metavar="card",
                        help="Add board cards")
    parser.add_argument("-e", "--exact", action="store_true",
                        help="Find exact odds by enumerating every possible "
                        "board")
    parser.add_argument("-n", type=int, default=100000,
                        help="Run N Monte Carlo simulations")
    parser.add_argument("-i", "--input", type=str,
                        help="Read hole cards and boards from an input file. "
                        "Commandline arguments for hole cards and board will "
                        "be ignored")
    # Parse command line arguments and check for errors
    args = parser.parse_args()

    # Parse hole cards and board
    hole_cards, board = None, None
    if not args.input:
        hole_cards, board = parse_cards(args.cards, args.board)
    return hole_cards, args.n, args.exact, board, args.input

# Parses a line taken from the input file and returns the hole cards and board


def parse_file_args(line):
    if line is None or len(line) == 0:
        print(line)
        print("Invalid format")
        exit()
    values = line.split("|")
    if len(values) > 2 or len(values) < 1:
        print(line)
        print("Invalid format")
        exit()
    hole_cards = values[0].split()
    all_cards = list(hole_cards)
    board = None
    if len(values) == 2:
        board = values[1].split()
        all_cards.extend(board)
    error_check_cards(all_cards)
    return parse_cards(hole_cards, board)

# Parses hole cards and board


def parse_cards(cards, board):
    hole_cards = create_hole_cards(cards)
    if board:
        board = parse_board(board)
    return hole_cards, board


def error_check_cards(all_cards):
    card_re = re.compile('[AKQJT98765432][scdh]')
    for card in all_cards:
        if card != "?" and not card_re.match(card):
            print("Invalid card given.")
            exit()
        else:
            if all_cards.count(card) != 1 and card != "?":
                print("The cards given must be unique.")
                exit()

# Returns tuple of two-tuple hole_cards: e.g. ((As, Ks), (Ad, Kd), (Jh, Th))


def create_hole_cards(raw_hole_cards):
    # Checking that there are an even number of hole cards
    if (raw_hole_cards is None or len(raw_hole_cards) < 2 or
            len(raw_hole_cards) % 2):
        print("You must provide a non-zero even number of hole cards")
        exit()
    # Create two-tuples out of hole cards
    hole_cards, current_hole_cards = [], []
    for hole_card in raw_hole_cards:
        if hole_card != "?":
            current_card = Card(hole_card)
            current_hole_cards.append(current_card)
        else:
            current_hole_cards.append(None)
        if len(current_hole_cards) == 2:
            if None in current_hole_cards:
                if (current_hole_cards[0] is not None or
                        current_hole_cards[1] is not None):
                    print("Unknown hole cards must come in pairs")
                    exit()
            hole_cards.append((current_hole_cards[0], current_hole_cards[1]))
            current_hole_cards = []
    if hole_cards.count((None, None)) > 1:
        print("Can only have one set of unknown hole cards")
    return tuple(hole_cards)

# Returns list of board cards: e.g. [As Ks Ad Kd]


def parse_board(board):
    if len(board) > 5 or len(board) < 3:
        print("Board must have a length of 3, 4, or 5.")
        exit()
    if "?" in board:
        print("Board cannot have unknown cards")
        exit()
    return create_cards(board)

# Instantiates new cards from the arguments and returns them in a tuple


def create_cards(card_strings):
    return [Card(arg) for arg in card_strings]


class Card:
    # Takes in strings of the format: "As", "Tc", "6d"
    def __init__(self, card_string):
        value, self.suit = card_string[0], card_string[1]
        self.value = CARD_VALUES[value]
        self.suit_index = SUITS_INDEX[self.suit]

    def __str__(self):
        return CARDS_STR[14 - self.value] + self.suit

    def __repr__(self):
        return CARDS_STR[14 - self.value] + self.suit

    def __eq__(self, other):
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.value == other.value and self.suit == other.suit

# Returns deck of cards with all hole cards and board cards removed


def generate_deck(hole_cards, board):
    deck = []
    for suit in SUITS:
        for value in CARDS_STR:
            deck.append(Card(value + suit))
    taken_cards = []
    for hole_card in hole_cards:
        for card in hole_card:
            if card is not None:
                taken_cards.append(card)
    if board and len(board) > 0:
        taken_cards.extend(board)
    for taken_card in taken_cards:
        deck.remove(taken_card)
    return tuple(deck)

# Generate all possible hole card combinations


def generate_hole_cards(deck):
    import itertools
    return itertools.combinations(deck, 2)

# Generate num_iterations random boards


def generate_random_boards(deck, num_iterations, board_length):
    import random
    import time
    random.seed(time.time())
    for _ in range(num_iterations):
        yield random.sample(deck, 5 - board_length)

# Generate all possible boards


def generate_exhaustive_boards(deck, num_iterations, board_length):
    import itertools
    return itertools.combinations(deck, 5 - board_length)

# Returns a board of cards all with suit = flush_index


def generate_suit_board(flat_board, flush_index):
    histogram = [card.value for card in flat_board
                 if card.suit_index == flush_index]
    histogram.sort(reverse=True)
    return histogram

# Returns a list of two tuples of the form: (value of card, frequency of card)


def preprocess(histogram):
    return [(14 - index, frequency) for index, frequency in
            enumerate(histogram) if frequency]


# Takes an iterable sequence and returns two items in a tuple:
# 1: 4-long list showing how often each card suit appears in the sequence
# 2: 13-long list showing how often each card value appears in the sequence
def preprocess_board(flat_board):
    suit_histogram, histogram = [0] * 4, [0] * 13
    # Reversing the order in histogram so in the future, we can traverse
    # starting from index 0
    for card in flat_board:
        histogram[14 - card.value] += 1
        suit_histogram[card.suit_index] += 1
    return suit_histogram, histogram, max(suit_histogram)

# Returns tuple: (Is there a straight flush?, high card)


def detect_straight_flush(suit_board):
    contiguous_length, fail_index = 1, len(suit_board) - 5
    # Won't overflow list because we fail fast and check ahead
    for index, elem in enumerate(suit_board):
        current_val, next_val = elem, suit_board[index + 1]
        if next_val == current_val - 1:
            contiguous_length += 1
            if contiguous_length == 5:
                return True, current_val + 3
        else:
            # Fail fast if straight not possible
            if index >= fail_index:
                if (index == fail_index and next_val == 5 and
                        suit_board[0] == 14):
                    return True, 5
                break
            contiguous_length = 1
    return False,

# Returns the highest kicker available


def detect_highest_quad_kicker(histogram_board):
    for elem in histogram_board:
        if elem[1] < 4:
            return elem[0]

# Returns tuple: (Is there a straight?, high card)


def detect_straight(histogram_board):
    contiguous_length, fail_index = 1, len(histogram_board) - 5
    # Won't overflow list because we fail fast and check ahead
    for index, elem in enumerate(histogram_board):
        current_val, next_val = elem[0], histogram_board[index + 1][0]
        if next_val == current_val - 1:
            contiguous_length += 1
            if contiguous_length == 5:
                return True, current_val + 3
        else:
            # Fail fast if straight not possible
            if index >= fail_index:
                if (index == fail_index and next_val == 5 and
                        histogram_board[0][0] == 14):
                    return True, 5
                break
            contiguous_length = 1
    return False,

# Returns tuple of the two highest kickers that result from the three of a kind


def detect_three_of_a_kind_kickers(histogram_board):
    kicker1 = -1
    for elem in histogram_board:
        if elem[1] != 3:
            if kicker1 == -1:
                kicker1 = elem[0]
            else:
                return kicker1, elem[0]

# Returns the highest kicker available


def detect_highest_kicker(histogram_board):
    for elem in histogram_board:
        if elem[1] == 1:
            return elem[0]

# Returns tuple: (kicker1, kicker2, kicker3)


def detect_pair_kickers(histogram_board):
    kicker1, kicker2 = -1, -1
    for elem in histogram_board:
        if elem[1] != 2:
            if kicker1 == -1:
                kicker1 = elem[0]
            elif kicker2 == -1:
                kicker2 = elem[0]
            else:
                return kicker1, kicker2, elem[0]

# Returns a list of the five highest cards in the given board
# Note: Requires a sorted board to be given as an argument


def get_high_cards(histogram_board):
    return histogram_board[:5]

# Return Values:
# Royal Flush: (9,)
# Straight Flush: (8, high card)
# Four of a Kind: (7, quad card, kicker)
# Full House: (6, trips card, pair card)
# Flush: (5, [flush high card, flush second high card, ..., flush low card])
# Straight: (4, high card)
# Three of a Kind: (3, trips card, (kicker high card, kicker low card))
# Two Pair: (2, high pair card, low pair card, kicker)
# Pair: (1, pair card, (kicker high card, kicker med card, kicker low card))
# High Card: (0, [high card, second high card, third high card, etc.])


def detect_hand(hole_cards, given_board, suit_histogram,
                full_histogram, max_suit):
    # Determine if flush possible. If yes, four of a kind and full house are
    # impossible, so return royal, straight, or regular flush.
    if max_suit >= 3:
        flush_index = suit_histogram.index(max_suit)
        for hole_card in hole_cards:
            if hole_card.suit_index == flush_index:
                max_suit += 1
        if max_suit >= 5:
            flat_board = list(given_board)
            flat_board.extend(hole_cards)
            suit_board = generate_suit_board(flat_board, flush_index)
            result = detect_straight_flush(suit_board)
            if result[0]:
                return (8, result[1]) if result[1] != 14 else (9,)
            return 5, get_high_cards(suit_board)

    # Add hole cards to histogram data structure and process it
    full_histogram = full_histogram[:]
    for hole_card in hole_cards:
        full_histogram[14 - hole_card.value] += 1
    histogram_board = preprocess(full_histogram)

    # Find which card value shows up the most and second most times
    current_max, max_val, second_max, second_max_val = 0, 0, 0, 0
    for item in histogram_board:
        val, frequency = item[0], item[1]
        if frequency > current_max:
            second_max, second_max_val = current_max, max_val
            current_max, max_val = frequency, val
        elif frequency > second_max:
            second_max, second_max_val = frequency, val

    # Check to see if there is a four of a kind
    if current_max == 4:
        return 7, max_val, detect_highest_quad_kicker(histogram_board)
    # Check to see if there is a full house
    if current_max == 3 and second_max >= 2:
        return 6, max_val, second_max_val
    # Check to see if there is a straight
    if len(histogram_board) >= 5:
        result = detect_straight(histogram_board)
        if result[0]:
            return 4, result[1]
    # Check to see if there is a three of a kind
    if current_max == 3:
        return 3, max_val, detect_three_of_a_kind_kickers(histogram_board)
    if current_max == 2:
        # Check to see if there is a two pair
        if second_max == 2:
            return 2, max_val, second_max_val, detect_highest_kicker(
                histogram_board)
        # Return pair
        else:
            return 1, max_val, detect_pair_kickers(histogram_board)
    # Check for high cards
    return 0, get_high_cards(histogram_board)

# Returns the index of the player with the winning hand


def compare_hands(result_list):
    best_hand = max(result_list)
    winning_player_index = result_list.index(best_hand) + 1
    # Check for ties
    if best_hand in result_list[winning_player_index:]:
        return 0
    return winning_player_index

# Print results


def print_results(hole_cards, winner_list, result_histograms):
    float_iterations = float(sum(winner_list))
    print("Winning Percentages:")
    for index, hole_card in enumerate(hole_cards):
        winning_percentage = round(float(winner_list[index + 1]) / float_iterations, PRECISION)
        if hole_card == (None, None):
            print("(?, ?) : ", winning_percentage)
        else:
            print(hole_card, ": ", winning_percentage)
    print("Ties: ", round(float(winner_list[0]) / float_iterations, PRECISION), "\n")
    for player_index, histogram in enumerate(result_histograms):
        print("Player" + str(player_index + 1) + " Histogram: ")
        for index, elem in enumerate(histogram):
            print(HAND_RANKINGS[index], ": ", round(float(elem) / float_iterations, PRECISION))
        print

# Returns the winning percentages


def find_winning_percentage(winner_list):
    float_iterations = float(sum(winner_list))
    percentages = []
    for num_wins in winner_list:
        winning_percentage = round(float(num_wins) / float_iterations, PRECISION)
        percentages.append(winning_percentage)
    return percentages

# Populate provided data structures with results from simulation


def find_winner(generate_boards, deck, hole_cards, num, board_length,
                given_board, winner_list, result_histograms):
    # Run simulations
    result_list = [None] * len(hole_cards)
    for remaining_board in generate_boards(deck, num, board_length):
        # Generate a new board
        if given_board:
            board = given_board[:]
            board.extend(remaining_board)
        else:
            board = remaining_board
        # Find the best possible poker hand given the created board and the
        # hole cards and save them in the results data structures
        suit_histogram, histogram, max_suit = (
            preprocess_board(board))
        for index, hole_card in enumerate(hole_cards):
            result_list[index] = detect_hand(hole_card, board, suit_histogram,
                                             histogram, max_suit)
        # Find the winner of the hand and tabulate results
        winner_index = compare_hands(result_list)
        winner_list[winner_index] += 1
        # Increment what hand each player made
        for index, result in enumerate(result_list):
            result_histograms[index][result[0]] += 1
