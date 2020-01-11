import random
import pprint
from connect5.agent.base import Agent
from connect5.board import GameState, Move
from connect5.types import Player, Point

import time

def get_diagonals(point):
    return [
        Point(point.row + 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row - 1, point.col - 1),
    ]

# 임의의 위치에 돌을 놓는 에이전트
def presuggestion(game_state, moves):
    # GameState, Move[] -> (best_move: Move, applied_gs: GameState)
    board = game_state.board
    num_rows = board.num_rows + 1
    num_cols = board.num_cols + 1

    # iterate all moveable moves
    for move in moves:
        center_point = move.point

        get_color = lambda p: board.get(p)

        center_color = get_color(center_point)

        # center_point 한 칸 위의 돌(col + 1)
        if (center_point.col + 1 > num_cols):
            top_point = None
        else:
            top_point = Point(center_point.row, center_point.col + 1)
        top_color = get_color(top_point)

        # center_point 한 칸 아래의 돌(col - 1)
        bottom_point = Point(center_point.row, center_point.col - 1)
        bottom_color = get_color(bottom_point)

        # center_point 한 칸 왼쪽의 돌(row - 1)
        left_point = Point(center_point.row - 1, center_point.col)
        left_color = get_color(left_point)

        # center_point 한 칸 왼쪽의 돌(row + 1)
        if (center_point.row + 1 > num_rows):
            right_point = None
        else:
            right_point = Point(center_point.row + 1, center_point.col)
        right_color = get_color(right_point)

        if (top_color == center_color == bottom_color):
            print('3 in a row, top to bottom!')

        if (left_color == center_color == right_color):
            print('3 in a row, left to right!')

        print(center_point, top_point, bottom_point, left_point, right_point)

    return None
