from connect5.types import Point

class Move:
    def __init__(self, point=None):
        assert Point is not None

        self.point = point

    def __str__(self):
        return f'(r {self.point.row}, c {self.point.col})'