from __future__ import print_function
from connect5 import board as connect5_board
from connect5 import types
from connect5.utils import print_board, print_move, point_from_coords
from connect5.C302 import C302Bot, presuggestion
from six.moves import input

def main():
    board_size = 8
    game = connect5_board.GameState.new_game(board_size)
    bot = C302Bot(1000, 1.01, presuggestion, 3, 0.4, 5)

    while not game.is_over():
        print_board(game.board)
        if game.next_player == types.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = connect5_board.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)

    print_board(game.board)

    if game.winner is "Draw":
        print("Draw!")
    else:
        print("Winner is %s!" % game.winner)

if __name__ == '__main__':
    main()