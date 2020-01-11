import math
import random

from connect5 import agent
from connect5.types import Player


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
        if child is not None:
            self.unvisited_moves = [move for move in self.unvisited_moves if move.point != child[1].point]
            new_node = MCTSNode(child[0], self, child[1])
            self.children.append(new_node)
            return new_node
        else:
            return self.add_random_child()


# MCTS 탐색 결과로 돌을 놓는 에이전트
class C302Bot(agent.Agent):
    # 초기화 메소드
    def __init__(self, num_rounds, temperature, suggestion_function):
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
                node = node.add_suggested_child_or_random(self.suggestion_function(node.game_state, node.unvisited_moves))

            winner = self.simulate_random_game(node.game_state)
            while node is not None:
                node.record_win(winner)
                node = node.parent

        self.cached_tree = root

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