from connect5.types import (
  BLACK,
  WHITE,
  Player,
)

p1 = Player(BLACK)
p2 = Player(WHITE)

assert p1.other == Player.white
assert p2.other == Player.black
