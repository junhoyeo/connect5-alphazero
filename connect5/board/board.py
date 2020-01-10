from connect5 import zobrist


class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = [x for x in [[0] * (self.num_cols + 1)] * (self.num_rows + 1)]
        self._hash = zobrist.EMPTY_BOARD

    def place_stone(self, player, point):
        assert self.is_valid_point(point)
        assert self.is_empty_slot(point)

        self._grid[point.row][point.col] = player

    def is_valid_point(self, point):
        is_on_valid_rows = 1 <= point.row <= self.num_rows
        is_on_valid_cols = 1 <= point.col <= self.num_cols

        return is_on_valid_rows and is_on_valid_cols

    def get(self, point):
        return self._grid[point.row][point.col]

    def zobrist_hash(self):
        return self._hash

    def is_empty_slot(self, point):
        return self.get(point) is 0