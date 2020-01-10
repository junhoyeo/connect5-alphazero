import random
import pprint
from connect5.agent.base import Agent
from connect5.board import Move
from connect5.types import Player, Point

# 임의의 위치에 돌을 놓는 에이전트
class RandomBot(Agent):
    # 행동을 선택하는 메소드
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        # 빈 자리 중에서 가중치를 계산함

        # presuggestion
        # 자기 색 돌은 +1, 다른 색 돌은 -1, 돌 3개가 연달아 있을 경우 양옆 -50
        num_rows = game_state.board.num_rows + 1
        num_cols = game_state.board.num_cols + 1
        candidates = []
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

                # 다른 사람 돌이 세 개 이상, 가로 또는 세로로
                center = game_state.board._grid[r][c]
                # same with row - 1, row + 1
                if game_state.board.get(neighbors[0]) == center and \
                    game_state.board.get(neighbors[1]) == center:

                    start = neighbors[0].neighbors()[0]
                    weights[start.row][start.col] -= 50

                    end = neighbors[1].neighbors()[1]
                    if end.row <= game_state.board.num_rows:
                        weights[end.row][end.col] -= 50

                # same with col - 1, col + 1
                if game_state.board.get(neighbors[2]) == center and \
                    game_state.board.get(neighbors[3]) == center:

                    start = neighbors[2].neighbors()[2]
                    weights[start.row][start.col] -= 50

                    end = neighbors[3].neighbors()[3]
                    if end.col <= game_state.board.num_cols:
                        weights[end.row][end.col] -= 50

        pprint.pprint(weights)
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
            print(best_candidate, min_weight)
            return Move.play(best_candidate)

        # weights 중 가장 가중치가 작은 좌표(음수)부터 0까지,
        # valid move인지 검증하고 candidates에 추가
        # pprint.pprint(weights)
        # @TODO: 랜덤으로 뽑지 말고 가장 가중치 낮은 칸부터

        else:
            for r in range(1, game_state.board.num_rows + 1):
                for c in range(1, game_state.board.num_cols + 1):
                    candidate = Point(row=r, col=c)
                    if game_state.is_valid_move(Move.play(candidate)):
                        candidates.append(candidate)
        return Move.play(random.choice(candidates))
