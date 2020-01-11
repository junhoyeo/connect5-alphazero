from connect5.board import Move
from connect5.types import Point

def get_diagonals(point):
    return [
        Point(point.row + 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row - 1, point.col - 1),
    ]

# 임의의 위치에 돌을 놓는 에이전트
def presuggestion(game_state):
    '''가중치 계산을 통해 행동 선택'''

    # 빈 자리 중에서 가중치를 계산함

    # presuggestion
    # 자기 색 돌은 +1, 다른 색 돌은 -1, 돌 3개가 연달아 있을 경우 양옆 -50
    num_rows = game_state.board.num_rows + 1
    num_cols = game_state.board.num_cols + 1
    weights = [x[:] for x in [[0] * num_cols] * num_rows]

    for r in range(1, num_rows - 1):
        for c in range(1, num_cols - 1):
            neighbors = Point(row=r, col=c).neighbors()
            for neighbor in neighbors:
                # 자기 돌
                if game_state.board._grid[r][c] == game_state.next_player:
                    # print(neighbor.row, neighbor.col)
                    weights[neighbor.row][neighbor.col] += 1
                # 다른 사람 돌
                elif game_state.board._grid[r][c] == game_state.next_player.other:
                    # print(neighbor.row, neighbor.col)
                    weights[neighbor.row][neighbor.col] -= 1

            # 다른 사람 돌이 세 개 이상
            if game_state.board._grid[r][c] == game_state.next_player.other:
                center = game_state.board._grid[r][c]

                # 가로 또는 세로로

                # same with row - 1, row + 1
                if game_state.board.get(neighbors[0]) == center and \
                    game_state.board.get(neighbors[1]) == center:

                    start = neighbors[0].neighbors()[0]
                    # only decrease weight when this is current problem
                    if start.col <= game_state.board.num_cols and \
                        start.row <= game_state.board.num_rows:
                        if weights[start.row][start.col] != game_state.next_player:
                            weights[start.row][start.col] -= 50

                    end = neighbors[1].neighbors()[1]
                    if end.col <= game_state.board.num_cols and \
                        end.row <= game_state.board.num_rows:
                        if weights[end.row][end.col] != game_state.next_player:
                            weights[end.row][end.col] -= 50

                # same with col - 1, col + 1
                if game_state.board.get(neighbors[2]) == center and \
                    game_state.board.get(neighbors[3]) == center:

                    start = neighbors[2].neighbors()[2]
                    if start.col <= game_state.board.num_cols and \
                        start.row <= game_state.board.num_rows:
                        if weights[start.row][start.col] != game_state.next_player:
                            weights[start.row][start.col] -= 50

                    end = neighbors[3].neighbors()[3]
                    if end.col <= game_state.board.num_cols and \
                        end.row <= game_state.board.num_rows:
                        if weights[end.row][end.col] != game_state.next_player:
                            weights[end.row][end.col] -= 50

                # 대각선으로 세 개
                diagonals = get_diagonals(Point(row=r, col=c))
                # / 오른쪽 향한 대각선으로

                if game_state.board.get(diagonals[0]) == center and \
                    game_state.board.get(diagonals[3]) == center:

                    start = get_diagonals(diagonals[0])[0]
                    if start.col <= game_state.board.num_cols and \
                        start.row <= game_state.board.num_rows:
                        if weights[start.row][start.col] != game_state.next_player:
                            weights[start.row][start.col] -= 50

                    end = get_diagonals(diagonals[3])[3]
                    if end.col <= game_state.board.num_cols and \
                        end.row <= game_state.board.num_rows:
                        if weights[end.row][end.col] != game_state.next_player:
                            weights[end.row][end.col] -= 50

                # \ 왼쪽 향한 대각선으로
                if game_state.board.get(diagonals[1]) == center and \
                    game_state.board.get(diagonals[2]) == center:

                    start = get_diagonals(diagonals[1])[1]
                    if start.col <= game_state.board.num_cols and \
                        start.row <= game_state.board.num_rows:
                        if weights[start.row][start.col] != game_state.next_player:
                            weights[start.row][start.col] -= 50

                    end = get_diagonals(diagonals[2])[2]
                    if end.col <= game_state.board.num_cols and \
                        end.row <= game_state.board.num_rows:
                        if weights[end.row][end.col] != game_state.next_player:
                            weights[end.row][end.col] -= 50

    min_weight = 100
    best_candidate = None
    for r in range(1, num_rows - 1):
        for c in range(1, num_cols - 1):
            if weights[r][c] < min_weight:
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)):
                    min_weight = weights[r][c]
                    best_candidate = candidate
    if min_weight < 0:
        #return Move.play(best_candidate)
        return (
            game_state.apply_move(Move.play(best_candidate)),
            Move.play(best_candidate),
        )
    return None

    # # pprint.pprint(weights)
    # min_weight = 100
    # candidates = []

    # for r in range(1, num_rows - 1):
    #     for c in range(1, num_cols - 1):
    #         if weights[r][c] < min_weight:
    #             candidate = Point(row=r, col=c)
    #             if game_state.is_valid_move(Move.play(candidate)):
    #                 min_weight = weights[r][c]

    # if min_weight < 100:
    #     for r in range(1, num_rows - 1):
    #         for c in range(1, num_cols - 1):
    #             if weights[r][c] == min_weight:
    #                 candidates.append(Point(row=r, col=c))

    # if not candidates:
    #     for r in range(1, game_state.board.num_rows + 1):
    #         for c in range(1, game_state.board.num_cols + 1):
    #             candidate = Point(row=r, col=c)
    #             if game_state.is_valid_move(Move.play(candidate)):
    #                 candidates.append(candidate)

    # return [
    #     (
    #         game_state.apply_move(Move.play(candidate)),
    #         Move.play(candidate),
    #     )
    #     for candidate in candidates
    # ]
