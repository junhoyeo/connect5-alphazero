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

    # point 한 칸 위의 돌(row + 1)
    def get_top_of_point(point):
        if (point.row + 1 >= num_rows):
            return None
        top = Point(point.row + 1, point.col)
        top_color = get_color(top)
        if top_color == 0:
            return None
        return (top, top_color)

    # point 한 칸 아래의 돌(row - 1)
    def get_bottom_of_point(point):
        bottom = Point(point.row - 1, point.col)
        bottom_color = get_color(bottom)
        if bottom_color == 0:
            return None
        return (bottom, bottom_color)

    # point 한 칸 오른쪽의 돌(col + 1)
    def get_right_of_point(point):
        if (point.col + 1 >= num_cols):
            return None
        right = Point(point.row, point.col + 1)
        right_color = get_color(right)
        if right_color == 0:
            return None
        return (right, right_color)

    # point 한 칸 왼쪽의 돌(col + 1)
    def get_left_of_point(point):
        left = Point(point.row, point.col - 1)
        left_color = get_color(left)
        if left_color == 0:
            return None
        return (left, left_color)

    # 오른쪽 위로 대각선
    def get_diagonal_top_right_of_point(point):
        if (point.row + 1 >= num_rows):
            return None
        if (point.col + 1 >= num_cols):
            return None
        diagonal = Point(point.row + 1, point.col + 1)
        diagonal_color = get_color(diagonal)
        if diagonal_color == 0:
            return None
        return (diagonal, diagonal_color)

    # 오른쪽 아래로 대각선
    def get_diagonal_bottom_right_of_point(point):
        if (point.col + 1 >= num_cols):
            return None
        diagonal = Point(point.row - 1, point.col + 1)
        diagonal_color = get_color(diagonal)
        if diagonal_color == 0:
            return None
        return (diagonal, diagonal_color)

    # 왼쪽 위로 대각선
    def get_diagonal_top_left_of_point(point):
        if (point.row + 1 >= num_rows):
            return None
        diagonal = Point(point.row + 1, point.col - 1)
        diagonal_color = get_color(diagonal)
        if diagonal_color == 0:
            return None
        return (diagonal, diagonal_color)

    # 왼쪽 아래로 대각선
    def get_diagonal_bottom_left_of_point(point):
        diagonal = Point(point.row - 1, point.col - 1)
        diagonal_color = get_color(diagonal)
        if diagonal_color == 0:
            return None
        return (diagonal, diagonal_color)

    def check_abstract(point, getter):
        match_color = None
        is_exist = None
        for idx in range(3):
            is_exist = getter(point)
            if is_exist:
                point, this_color = is_exist
                # print(f'T{idx}', is_exist)
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

        # 위에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_top_of_point):
            print(f'{current_point} 위에 돌 세 개가 있습니다.')

        # 아래에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_bottom_of_point):
            print(f'{current_point} 아래에 돌 세 개가 있습니다.')

        # 오른쪽에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_left_of_point):
            print(f'{current_point} 오른쪽에 돌 세 개가 있습니다.')

        # 왼쪽에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_right_of_point):
            print(f'{current_point} 왼쪽에 돌 세 개가 있습니다.')

        # 대각선 오른쪽 위에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_top_right_of_point):
            print(f'{current_point} 대각선 오른쪽 위에 돌 세 개가 있습니다.')

        # 대각선 오른쪽 아래에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_bottom_right_of_point):
            print(f'{current_point} 대각선 오른쪽 아래에 돌 세 개가 있습니다.')

        # 대각선 왼쪽 위에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_top_left_of_point):
            print(f'{current_point} 대각선 왼쪽 위에 돌 세 개가 있습니다.')

        # 대각선 완쪽 아래에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_bottom_left_of_point):
            print(f'{current_point} 대각선 왼쪽 아래에 돌 세 개가 있습니다.')

    return None
