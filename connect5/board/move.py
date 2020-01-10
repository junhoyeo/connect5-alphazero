from connect5.types import Point

class Move:
  def __init__(self, point: Point or None = None):
    assert (Point is not None)
    self.point = point

  @classmethod
  def play(cls, point: Point):
    return Move(point=point)

  def __str__(self):
    return f'(r {self.point.row}, c {self.point.col})'
