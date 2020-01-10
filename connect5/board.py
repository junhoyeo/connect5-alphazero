import copy
from connect5.types import (
  Player,
  Point,
  Direction,
)
from connect5 import zobrist

class Board:
  def __init__(self, num_rows: int, num_cols: int) -> None:
    self.num_rows = num_rows
    self.num_cols = num_cols
    self._grid = [
      x
      for x in [[0] * (self.num_cols + 1)] * (self.num_rows + 1)
    ]
    self._hash = zobrist.EMPTY_BOARD

  def place_stone(self, player: Player, point: Point) -> None:
    assert self.is_on_grid(point)

    stone_location = self._grid[point.row][point.col]
    assert stone_location is 0
    stone_location = player

  def is_on_grid(self, point: Point) -> bool:
    is_in_rows = 1 <= point.row <= self.num_rows
    is_in_cols = 1 <= point.col <= self.num_cols
    return is_in_rows and is_in_cols

  def get(self, point: Point) -> Player:
    stone_color = self._grid[point.row][point.col]
    assert stone_color in [0, 1, 2]
    return stone_color

  def zobrist_hash(self) -> int:
    return self._hash

class Move:
  def __init__(self, point: Point | None = None):
    assert (Point is not None)
    self.point = point

  @classmethod
  def play(cls, point: Point):
    return Move(point=point)

  def __str__(self):
    return f'(r {self.point.row}, c {self.point.col})'
