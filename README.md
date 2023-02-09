# poker

========== Nash Equilibrium Push or Fold Tables ==========

https://www.holdemresources.net/hune
https://matchpoker.com/learn/strategy-guides/push-fold-charts
https://www.push-or-fold.com/gb/jennifear-push-fold.php

========== TREYS ==========

A pure Python poker hand evaluation library

https://github.com/ihendley/treys

Treys is a Python 3 port of Deuces based on the initial work in msaindon’s fork. Deuces was written by Will Drevo for the MIT Pokerbots Competition.

Treys is lightweight and fast. All lookups are done with bit arithmetic and dictionary lookups. That said, Treys won’t beat a C implemenation (~250k eval/s) but it is useful for situations where Python is required or where bots are allocated reasonable thinking time (human time scale).

Treys handles 5, 6, and 7 card hand lookups. The 6 and 7 card lookups are done by combinatorially evaluating the 5 card choices.

'''
board = [
treys.Card.new('Ah'),
treys.Card.new('Kd'),
treys.Card.new('Jc')
]
player_hand = [
treys.Card.new('Qs'),
treys.Card.new('Th')
]

treys.Card.print_pretty_cards(board + player_hand)

evaluator = treys.Evaluator()
player_score = evaluator.evaluate(board, player_hand)
player_class = evaluator.get_rank_class(player_score)

print(player_score)
print(player_class)

print("Player 1 hand rank = %d (%s)\n" % (player_score, evaluator.class_to_string(player_class)))

'''

========== POKER EDGE ==========
Online Poker Odds Calculator, Analyzer & Helper for Texas Hold'Em
https://app.edge.poker/advanced/
