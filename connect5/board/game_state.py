import copy
from connect5.board import Board
from connect5.types import Player, Point, Direction
from .move import Move


class GameState:
    def __init__(self, board, next_player, previous):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous

        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states | {(previous.next_player, previous.board.zobrist_hash())}
            )
        self.winner = None

    def apply_move(self, move):
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(self.next_player, move.point)

        return GameState(next_board, self.next_player.other, self)

    @staticmethod
    def new_game(board_size):
        board = Board(num_rows=board_size, num_cols=board_size)

        return GameState(board, Player.black, None)

    def is_valid_move(self, move):
        return self.board.get(move.point) is 0

    def is_over_in(self, stone_color, row, row_add, col, col_add, direction):
        if self.board.is_on_grid(Point(row=row + row_add, col=col + col_add)) and \
                stone_color == self.board._grid[row + row_add, col + col_add]:
            if self.is_connect5(row, col, stone_color, direction):
                self.winner = 'Black' if stone_color == Player.black else 'White'
                return True

    def is_over(self):
        is_full = True
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                stone_color = self.board._grid[row][col]
                if stone_color != 0:
                    for (row_add, col_add, direction) in [
                        [0, 1, Direction.right],
                        [1, 0, Direction.down],
                        [1, 1, Direction.right_down],
                        [1, -1, Direction.left_down],
                    ]:
                        if self.is_over_in(stone_color, row, row_add, col, col_add, direction):
                            return True
                else:
                    is_full = False
            if is_full:
                self.winner = 'Draw'
                return True
            else:
                return False

    def is_connect5(self, r, c, stone_color, direction):
        if not self.is_middle(r, c, stone_color, direction):
            return False
        stones = [Point(r, c)]
        d_row = r
        d_col = c

        if direction is Direction.right:
            d_col += 1
            while self.board.is_on_grid(Point(row=d_row, col=d_col)) and \
                    self.board._grid[d_row][d_col] is stone_color:
                stones.append(Point(row=d_row, col=d_col))
                d_col += 1
        elif direction is Direction.down:
            d_row += 1
            while self.board.is_on_grid(Point(row=d_row, col=d_col)) and \
                    self.board._grid[d_row][d_col] is stone_color:
                stones.append(Point(row=d_row, col=d_col))
                d_row += 1
        elif direction is Direction.right_down:
            d_row += 1
            d_col += 1
            while self.board.is_on_grid(Point(row=d_row, col=d_col)) and \
                    self.board._grid[d_row][d_col] is stone_color:
                stones.append(Point(row=d_row, col=d_col))
                d_row += 1
                d_col += 1
        elif direction is Direction.left_down:
            d_row += 1
            d_col -= 1
            while self.board.is_on_grid(Point(row=d_row, col=d_col)) and \
                    self.board._grid[d_row][d_col] is stone_color:
                stones.append(Point(row=d_row, col=d_col))
                d_row += 1
                d_col -= 1
        return len(stones) is 4

    def is_middle(self, r, c, stone_color, direction):
        for [row_add, col_add, _direction] in [
            [0, -1, Direction.right],
            [-1, 0, Direction.down],
            [-1, -1, Direction.right_down],
            [-1, 1, Direction.left_down],
        ]:
            if direction is Direction.right and self.board.is_on_grid(
                    Point(row=r + row_add, col=c + col_add)
            ):
                if self.board._grid[r + row_add, c + col_add] == stone_color:
                    return False
        return True

    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        return moves
