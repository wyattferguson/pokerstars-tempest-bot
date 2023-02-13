from collections import Counter, namedtuple

from config import *

RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
Card = namedtuple('Card', ['suit', 'rank'])


class Hand:
    def __init__(self, hand):
        self.hand = hand
        self.catg = None
        self.high_card_ranks = []
        self.hand.sort(key=(lambda c: c.rank), reverse=True)
        self._classify_hand()

    def __eq__(self, x_hand):
        return self._comp_hand(x_hand) == 'EQ'

    def __lt__(self, x_hand):
        return self._comp_hand(x_hand) == 'LT'

    def __gt__(self, x_hand):
        return self._comp_hand(x_hand) == 'GT'

    def list_format(self):
        tmp = []
        for c in self.hand:
            tmp.append(str(FACE_CARDS.get(c.rank, c.rank)) + c.suit)
        return tmp

    def str_format(self):
        repr_str = ''
        for c in self.hand:
            repr_str += str(FACE_CARDS.get(c.rank, c.rank)) + c.suit
        return repr_str

    def __repr__(self):
        repr_str = ''
        for n in range(0, 5):
            repr_str += str(FACE_CARDS.get(self.hand[n].rank,
                                           self.hand[n].rank)) \
                + self.hand[n].suit + ' '
        return repr_str

    def get_cards(self) -> list[str]:
        cards = []
        for n in range(0, 5):
            tmp_card = f"{FACE_CARDS.get(self.hand[n].rank, self.hand[n].rank)}{self.hand[n].suit}"
            cards.append(tmp_card)

        return cards

    def _classify_hand(self):
        rank_freq = list(Counter(card.rank for card in self.hand).values())
        suit_freq = list(Counter(card.suit for card in self.hand).values())
        rank_freq.sort()
        suit_freq.sort()
        if self._is_straight() and suit_freq[0] == 5:
            self.catg = 'SF'
            self.high_card_ranks = [c.rank for c in self.hand]
            self._wheel_check()
        elif rank_freq[1] == 4:
            self.catg = '4K'
            self.high_card_ranks = [self.hand[2].rank,
                                    (self.hand[0].rank
                                     if self.hand[0].rank != self.hand[2].rank
                                     else self.hand[4].rank)]
        elif rank_freq[1] == 3:
            self.catg = 'FH'
            self.high_card_ranks = [self.hand[2].rank,
                                    (self.hand[3].rank
                                     if self.hand[3].rank != self.hand[2].rank
                                     else self.hand[1].rank)]
        elif suit_freq[0] == 5:
            self.catg = 'F'
            self.high_card_ranks = [c.rank for c in self.hand]
        elif self._is_straight():
            self.catg = 'S'
            self.high_card_ranks = [c.rank for c in self.hand]
            self._wheel_check()
        elif rank_freq[2] == 3:
            self.catg = '3K'
            self.high_card_ranks = [self.hand[4].rank, self.hand[0].rank]
            self.high_card_ranks.append(self.hand[3].rank
                                        if self.hand[1].rank in self.high_card_ranks
                                        else self.hand[1].rank)
        elif rank_freq[2] == 2:
            self.catg = '2K2'
            self.high_card_ranks = [self.hand[0].rank,
                                    self.hand[2].rank,
                                    self.hand[4].rank]
        elif rank_freq[3] == 2:
            self.catg = '2K'
            self.high_card_ranks = list(set(c.rank for c in self.hand))
        else:
            self.catg = None
            self.high_card_ranks = [c.rank for c in self.hand]

    def _is_straight(self):
        return ((False not in [(self.hand[n].rank == self.hand[n + 1].rank + 1)
                               for n in (0, 1, 2, 3)])
                or ([c.rank for c in self.hand] == [14, 5, 4, 3, 2]))

    def _wheel_check(self):
        # allows for the correct ordering of low ace ("wheel") straight
        if (self.catg in ['SF', 'S']
                and self.high_card_ranks == [14, 5, 4, 3, 2]):
            self.high_card_ranks.pop(0)
            self.high_card_ranks.append(1)

    def _comp_hand(self, comp_hand):
        ret_val = 'EQ'
        catg_order = [None, '2K', '2K2', '3K', 'S', 'F', 'FH', '4K', 'SF']
        curr_hand_catg = catg_order.index(self.catg)
        comp_hand_catg = catg_order.index(comp_hand.catg)
        if curr_hand_catg > comp_hand_catg:
            ret_val = 'GT'
        elif curr_hand_catg < comp_hand_catg:
            ret_val = 'LT'
        else:
            for curr_high_card, comp_high_card in \
                    zip(self.high_card_ranks, comp_hand.high_card_ranks):
                if curr_high_card > comp_high_card:
                    ret_val = 'GT'
                    break
                elif curr_high_card < comp_high_card:
                    ret_val = 'LT'
                    break
        return ret_val
