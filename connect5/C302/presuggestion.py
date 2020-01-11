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

    get_color = board.get
    is_on_grid = board.is_on_grid

    # point 한 칸 위의 돌(row + 1)
    def get_top_of_point(point):
        top = Point(point.row + 1, point.col)
        if not is_on_grid(top):
            return None
        top_color = get_color(top)
        return (top, top_color)

    # point 한 칸 아래의 돌(row - 1)
    def get_bottom_of_point(point):
        bottom = Point(point.row - 1, point.col)
        if not is_on_grid(bottom):
            return None
        bottom_color = get_color(bottom)
        return (bottom, bottom_color)

    # point 한 칸 오른쪽의 돌(col + 1)
    def get_right_of_point(point):
        right = Point(point.row, point.col + 1)
        if not is_on_grid(right):
            return None
        right_color = get_color(right)
        return (right, right_color)

    # point 한 칸 왼쪽의 돌(col + 1)
    def get_left_of_point(point):
        left = Point(point.row, point.col - 1)
        if not is_on_grid(left):
            return None
        left_color = get_color(left)
        return (left, left_color)

    # 오른쪽 위로 대각선
    def get_diagonal_top_right_of_point(point):
        diagonal = Point(point.row + 1, point.col + 1)
        if not is_on_grid(diagonal):
            return None
        diagonal_color = get_color(diagonal)
        return (diagonal, diagonal_color)

    # 오른쪽 아래로 대각선
    def get_diagonal_bottom_right_of_point(point):
        diagonal = Point(point.row - 1, point.col + 1)
        if not is_on_grid(diagonal):
            return None
        diagonal_color = get_color(diagonal)
        return (diagonal, diagonal_color)

    # 왼쪽 위로 대각선
    def get_diagonal_top_left_of_point(point):
        diagonal = Point(point.row + 1, point.col - 1)
        if not is_on_grid(diagonal):
            return None
        diagonal_color = get_color(diagonal)
        return (diagonal, diagonal_color)

    # 왼쪽 아래로 대각선
    def get_diagonal_bottom_left_of_point(point):
        diagonal = Point(point.row - 1, point.col - 1)
        if not is_on_grid(diagonal):
            return None
        diagonal_color = get_color(diagonal)
        return (diagonal, diagonal_color)

    def check_abstract(point, getter, offset=3):
        match_color = game_state.next_player.other
        for _ in range(offset):
            is_exist = getter(point)
            if is_exist:
                point, this_color = is_exist
                if match_color != this_color:
                    return False
            else:
                return False
        if offset == 3:
            is_exist = getter(point)
            if is_exist:
                _, this_color = is_exist
                if match_color.other == this_color:
                    return False
        return True

    # point를 기준으로 getter가 생성하는 새로운 돌이 얼만큼 이어지는지 셈
    def check_count(point, getter):
        match_color = game_state.next_player.other
        count = 0
        while 1:
            is_exist = getter(point)
            if is_exist:
                point, this_color = is_exist
                if match_color != this_color:
                    break
                count += 1
            else:
                break
        return count

    def check_between_one(point, getter_pre, getter_post):
        check_pre = check_count(point, getter_pre)
        check_post = check_count(point, getter_post)
        count = check_pre + check_post

        if (check_pre == 0) or (check_post == 0) or (count >= 5) or (count < 3):
            return False
        if count == 3:
            match_color = game_state.next_player.other
            pre_point = point
            for _ in range(check_pre):
                is_exist = getter_pre(pre_point)
                if is_exist:
                    pre_point, this_color = is_exist
                    if match_color.other == this_color:
                        return False
            post_point = point
            for _ in range(check_post):
                is_exist = getter_post(post_point)
                if is_exist:
                    post_point, this_color = is_exist
                    if match_color.other == this_color:
                        return False
            return True
        else:
            return True

    # iterate all moveable moves
    # print([m.point for m in moves])
    suggestions = []
    for move in moves:
        current_point = move.point

        # 위에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_top_of_point):
            suggestions.append(current_point)

        # 아래에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_bottom_of_point):
            suggestions.append(current_point)

        if check_between_one(current_point, get_top_of_point, get_bottom_of_point):
            suggestions.append(current_point)

        # 오른쪽에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_left_of_point):
            suggestions.append(current_point)

        # 왼쪽에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_right_of_point):
            suggestions.append(current_point)

        if check_between_one(current_point, get_right_of_point, get_left_of_point):
            suggestions.append(current_point)

        # 대각선 오른쪽 위에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_top_right_of_point):
            suggestions.append(current_point)

        # 대각선 왼쪽 위에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_top_left_of_point):
            suggestions.append(current_point)

        if check_between_one(current_point, get_diagonal_top_right_of_point, get_diagonal_bottom_left_of_point):
            suggestions.append(current_point)

        # 대각선 오른쪽 아래에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_bottom_right_of_point):
            suggestions.append(current_point)

        # 대각선 완쪽 아래에 같은 색 돌 세 개가 있나 체크
        if check_abstract(current_point, get_diagonal_bottom_left_of_point):
            suggestions.append(current_point)

        if check_between_one(current_point, get_diagonal_bottom_right_of_point, get_diagonal_top_left_of_point):
            suggestions.append(current_point)

    max_freq = 0
    if len(suggestions) == 0:
        return None
    for suggest in suggestions:
        freq = len([s for s in suggestions if s.row == suggest.row and s.col == suggest.col])
        if freq > max_freq:
            max_freq = freq
            chosen = suggest
    return (
        game_state.apply_move(Move.play(chosen)),
        Move.play(chosen),
    )
