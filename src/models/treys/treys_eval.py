from treys import Card, Evaluator

if __name__ == "__main__":
    board = [
        Card.new('Ah'),
        Card.new('Kd'),
        Card.new('Jc')
    ]
    player_hand = [
        Card.new('Qs'),
        Card.new('Th')
    ]

    Card.print_pretty_cards(board + player_hand)

    evaluator = Evaluator()
    player_score = evaluator.evaluate(board, player_hand)
    player_class = evaluator.get_rank_class(player_score)

    print(player_score)
    print(player_class)

    print("Player 1 hand rank = %d (%s)\n" % (player_score, evaluator.class_to_string(player_class)))
