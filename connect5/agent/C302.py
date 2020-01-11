import math
import random

from connect5 import agent
from connect5.types import Player
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



# 트리의 노드 클래스
class MCTSNode(object):
    # 초기화 메소드
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 0
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = game_state.legal_moves()

    # 노드에 무작위 자식 노드를 추가하는 메소드
    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    # 노드의 값을 갱신하는 메소드
    def record_win(self, winner):
        if winner is 0:
            self.win_counts[Player.black] += 1
            self.win_counts[Player.white] += 1
        else:
            self.win_counts[winner] += 1
        self.num_rollouts += 1

    # 더 자식 노드를 추가할 수 있는지를 반환하는 메소드
    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    # 게임의 끝을 판단하는 메소드
    def is_terminal(self):
        return self.game_state.is_over()

    # 해당 노드의 승률을 구하는 메소드
    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)

    def fetch_cached_child(self, childable):
        for childP in self.children:
            for child in childP.children:
                if child.game_state.board._grid == childable.game_state.board._grid:
                    child.parent = None
                    return child
        return childable

    def add_suggested_child_or_random(self, child):
        if (child is not None) and child[1] in self.unvisited_moves:
            self.unvisited_moves.pop(self.unvisited_moves.index(child[1]))
            new_node = MCTSNode(child[0], self, child[1])
            self.children.append(new_node)
            return new_node
        else:
            return self.add_random_child()


# MCTS 탐색 결과로 돌을 놓는 에이전트
class C302Bot(agent.Agent):
    # 초기화 메소드
    def __init__(self, num_rounds, temperature, suggestion_function=presuggestion):
        agent.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature
        self.cached_tree = None
        self.suggestion_function = suggestion_function

    # 현재 게임 상태에서 다음 돌을 놓을 위치를 결정하는 메소드
    def select_move(self, game_state):
        root = MCTSNode(game_state)
        if self.cached_tree is not None:
            root = self.cached_tree.fetch_cached_child(root)

        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_suggested_child_or_random(self.suggestion_function(node.game_state))

            winner = self.simulate_random_game(node.game_state)
            while node is not None:
                node.record_win(winner)
                node = node.parent

        self.cached_tree = root

        scored_moves = [
            (child.winning_frac(game_state.next_player), child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    # 탐색할 자식 노드를 선택하는 메소드
    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None

        for child in node.children:
            win_percentage = child.winning_frac(node.game_state.next_player)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor

            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    # 게임을 무작위 시뮬레이션 하는 메소드
    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.black: agent.RandomBot(),
            Player.white: agent.RandomBot(),
        }
        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)
        if game.winner is "Black":
            return Player.black
        elif game.winner is "White":
            return Player.white
        else:
            return 0