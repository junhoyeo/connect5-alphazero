from __future__ import print_function
from connect5 import board as connect5_board
from connect5 import types
from connect5.utils import print_board, print_move
from connect5.C302 import C302Bot, presuggestion


def main():
    board_size = 8
    game = connect5_board.GameState.new_game(board_size)
    bots = {
        types.Player.black: C302Bot(2500, 1.15, presuggestion),
        types.Player.white: C302Bot(2500, 1.15, presuggestion),
    }

    while not game.is_over():
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)

    print_board(game.board)

    if game.winner is "Draw":
        print("Draw!")
    else:
        print("Winner is %s!" % game.winner)

if __name__ == '__main__':
    main()