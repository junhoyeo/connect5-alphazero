import math
import random

from connect5 import agent
from connect5.types import Player


class MCTSNode(object):
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
        self.is_terminal = self.game_state.is_over()

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner): #No-touch
        self.num_rollouts += 1
        if winner is None:
            self.win_counts[Player.black] += 1
            self.win_counts[Player.white] += 1
        else:
            self.win_counts[winner] += 1

    def can_add_child(self):
        return (not self.is_terminal) and (len(self.unvisited_moves) > 0)

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)

    def add_suggested_child_or_random(self, suggestion):
        if suggestion is not None:
            suggested_game_state, suggested_move = suggestion
            self.unvisited_moves = [move for move in self.unvisited_moves if move.point != suggested_move.point]
            new_node = MCTSNode(suggested_game_state, self, suggested_move)
            self.children.append(new_node)
            print('suggestion received!') #debug
            print(new_node.move)
            return new_node
        else:
            return self.add_random_child()

    def is_leaf(self): #No-touch
        return len(self.children) == 0


class C302Bot(agent.Agent):
    def __init__(self, num_rounds, temperature, suggestion_function, least_infer_node_count=3, least_winning_frac=0.5):
        agent.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature
        self.cached_tree = None
        self.suggestion_function = suggestion_function
        self.least_infer_node_count = least_infer_node_count
        self.least_winning_frac = least_winning_frac

    def fetch_cached_root(self, game_state):
        if not (self.cached_tree is None):
            for childP in self.cached_tree.children:
                for child in childP.children:
                    if child.game_state.board._grid == game_state.board._grid:
                        child.parent = None
                        return child
        else:
            return None

    def select_move(self, game_state):
        root = self.fetch_cached_root(game_state)
        if root is None:
            root = MCTSNode(game_state)
        self.cached_tree = root

        for i in range(self.num_rounds):
            node = root
            while (not node.is_terminal) and (not node.is_leaf()):
                node, is_self = self.select_next_node(node, game_state.next_player)
                if is_self:
                    break

            if node.can_add_child():
                node = node.add_suggested_child_or_random(self.suggestion_function(node.game_state, node.unvisited_moves))

            winner = self.simulate_random_game(node.game_state)
            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_children(self, children):
        total_rollouts = sum(child.num_rollouts for child in children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None

        for child in children:
            win_percentage = child.winning_frac(child.parent.game_state.next_player) #test
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor

            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    def select_next_node(self, node, player):
        child_length = len(node.children)
        if (not (child_length >= (len(node.unvisited_moves) + child_length / self.least_infer_node_count))) or \
                ((sum(child.winning_frac(player) for child in node.children) / child_length) < self.least_winning_frac):
            return node, True
        else:
            return self.select_children(node.children), False

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
            return None