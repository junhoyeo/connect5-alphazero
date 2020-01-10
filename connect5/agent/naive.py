import random
from connect5.agent.base import Agent
from connect5.board import Move
from connect5.types import Player, Point

# 임의의 위치에 돌을 놓는 에이전트
class RandomBot(Agent):
    # 행동을 선택하는 메소드
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        # 빈 자리 중에서 가중치를 계산함
        # 자기 색 돌은 +1, 다른 색 돌은 -1, 돌 3개가 연달아 있을 경우 양옆 -50
        num_rows = game_state.board.num_rows + 1
        num_cols = game_state.board.num_cols + 1
        candidates = []
        weights = [x[:] for x in [[0] * num_cols] * num_rows]

        for r in range(1, num_rows - 1):
            for c in range(1, num_cols - 1):
                neighbors = Point(row=r, col=c).neighbors()
                for neighbor in neighbors:
                    if game_state.board._grid[r][c] == Player.white:
                        # print(neighbor.row, neighbor.col)
                        weights[neighbor.row][neighbor.col] += 1
                    elif game_state.board._grid[r][c] == Player.black:
                        # print(neighbor.row, neighbor.col)
                        weights[neighbor.row][neighbor.col] -= 1
                    # @TODO: 돌 3개 이상시 경우 추가

        for r in range(1, num_rows - 1):
            for c in range(1, num_cols - 1):
                if weights[r][c] < 0:
                    candidate = Point(row=r, col=c)
                    # print(candidate)
                    if game_state.is_valid_move(Move.play(candidate)):
                        # print(candidate)
                        candidates.append(candidate)
        # weights 중 가장 가중치가 작은 좌표(음수)부터 0까지,
        # valid move인지 검증하고 candidates에 추가
        # pprint.pprint(weights)
        # @TODO: 랜덤으로 뽑지 말고 가장 가중치 낮은 칸부터

        if not candidates:
            for r in range(1, game_state.board.num_rows + 1):
                for c in range(1, game_state.board.num_cols + 1):
                    candidate = Point(row=r, col=c)
                    if game_state.is_valid_move(Move.play(candidate)):
                        candidates.append(candidate)
        return Move.play(random.choice(candidates))
