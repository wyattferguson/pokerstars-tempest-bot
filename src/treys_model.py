from config import *
import treys

if __name__ == "__main__":
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
