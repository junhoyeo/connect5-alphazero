import random
import pprint
from connect5.agent.base import Agent
from connect5.board import GameState, Move
from connect5.types import Player, Point

import time

# def get_diagonals(point):
#     return [
#         Point(point.row + 1, point.col + 1),
#         Point(point.row + 1, point.col - 1),
#         Point(point.row - 1, point.col + 1),
#         Point(point.row - 1, point.col - 1),
#     ]

# 임의의 위치에 돌을 놓는 에이전트
def presuggestion(game_state, moves):
    # GameState, Move[] -> (best_move: Move, applied_gs: GameState)
    board = game_state.board
    num_rows = board.num_rows + 1
    num_cols = board.num_cols + 1

    get_color = lambda p: board.get(p)

    # point 한 칸 위의 돌(col + 1)
    def get_top_of_point(point):
        if (point.row + 1 >= num_rows):
            return None
        else:
            top = Point(point.row + 1, point.col)
            top_color = get_color(top)
            if top_color == 0:
                return None
        return (top, top_color)

    # 위에 같은 색 돌 세 개가 있나 체크
    def check_three_in_top(point):
        match_color = None
        is_top = None
        for idx in range(3):
            is_top = get_top_of_point(point)
            if is_top:
                point, this_color = is_top
                # print(f'T{idx}', is_top)
                if not idx:
                    match_color = this_color
                if match_color != this_color:
                    return False
            else:
                return False
        return True

    # iterate all moveable moves
    print([m.point for m in moves])
    for move in moves:
        current_point = move.point

        if check_three_in_top(current_point):
            print(current_point)

    return None
