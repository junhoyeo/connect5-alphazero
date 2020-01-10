# Test for Player

from connect5.types import (
  Player,
)

p1 = Player(1)
p2 = Player(2)

assert p1.other == Player.white
assert p2.other == Player.black

# Test for Board

from connect5.board import Board

board = Board(5, 5)
assert board._grid == [x for x in [[0] * 6] * 6]
