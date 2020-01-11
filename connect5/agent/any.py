import random
from connect5.agent.base import Agent
from connect5.board import Move
from connect5.types import Point


# 임의의 위치에 돌을 놓는 에이전트
class RandomBotA(Agent):
    # 행동을 선택하는 메소드
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes.
           우리 자신의 눈을 유지하는 임의의 유효한 움직임을 선택하십시오."""
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):  # 열
            for c in range(1, game_state.board.num_cols + 1):  # 행
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)):
                    candidates.append(candidate)
        return Move.play(random.choice(candidates))

    def Radius(position, board):
        # Return the discrete distance from given position to center

        size, x, y = board.size, *position
        return (abs(x - size // 2) + abs(y - size // 2))

    def Radius_Limit(board):
        length = len(board.report)
        max_rad = max(Radius(position, board) for position in board.report) + 2

        if length <= 10:
            lim_rad = 3
        elif length <= 20:
            lim_rad = 4
        else:
            lim_rad = max(int((length / 2) ** (0.5)) + 2, 6)

        return max(lim_rad, max_rad)

    def Rocks(board):
        # Return positions available
        size, pos_able, lim_rad = board.size, [], Radius_Limit(board)

        for x in range(size):
            for y in range(size):
                position = (x, y)
                if position in board.report:
                    continue
                rad = Radius(position, board)
                if rad <= lim_rad:
                    pos_able.append(position)
        return pos_able

    def Random(num, list_rock, board):
        # Return 'num' of random choices of list_rock
        if len(list_rock) <= num:
            return list_rock

        import random
        return random.sample(list_rock, num)  # Normal random function

    def Cover(sublist_rock, board):
        from base.omok_sub import Copy
        # Return the new board which is covered by rocks of positions in sublist,
        # covered rocks are numbered by 3
        covered = Copy(len(board.report), board)
        size = board.size
        for x in range(size):
            for y in range(size):
                if (x, y) in sublist_rock:
                    covered.state[x][y] = 3
        return covered

    def Turn2Win(position, color, board):
        from base import omok_basic, omok_sub
        if omok_basic.Win(position, color, board):
            return 0
        if omok_sub.Able(position, color, board):
            return 10

        directions, lengths, blocks = omok_sub.Max_Length2(position, color, board)
        cases = []
        for length, block in zip(lengths, blocks):
            if (block == 0 and length // 1 == 4) or (color == 2 and length in [4.5, 5]):
                cases.append((length // 1, block))
        if cases:
            return 1

        for length, block in zip(lengths, blocks):
            case = (length // 1, block)
            if case in [(3, 0), (4, 1)]:
                cases.append(case)
        if len(set(cases)) >= 2 or (color == 2 and len(cases) >= 2):
            return 1

        turns = []
        for length, block in zip(lengths, blocks):
            if block == 2:
                continue
            if length // 1 == 4:
                turns.append(2)
            elif length // 1 == 3:
                if length % 1 == 0.5:
                    turns.append(2)
            elif length // 1 >= 2:
                if length % 1 in [0.1, 0.2]:
                    turns.append(3)
            else:
                turns.append(5)
        return max(turns)

    def Point(rock, color, board):
        from base.omok_sub import Next_Color
        return 3 ** (5 - Turn2Win(rock, color, board)) + 2 ** (5 - Turn2Win(rock, Next_Color(color), board)) - 2

    def Haveto(color, board):
        from base.omok_basic import Win
        from base.omok_sub import Next_Color
        size, case_win, case_lose = board.size, [], []
        mycolor, yourcolor = color, Next_Color(color)

        for i in range(size):
            for j in range(size):
                if board.state[i][j] != 0:
                    continue
                if Win((i, j), mycolor, board):
                    case_win.append((i, j))
                if Turn2Win((i, j), yourcolor, board) <= 2:
                    case_lose.append((i, j))
        if case_win:
            return case_win[0]
        elif case_lose:
            points = [Point(pos, color, board) for pos in case_lose]
            return case_lose[points.index(max(points))]

    def Ai_Choice(color, board):
        N, num = 1000, 10
        list_rock = Rocks(board)
        points = {a: 0 for a in list_rock}

        position = Haveto(color, board)
        if position:
            return position

        for n in range(N):
            sublist_rock = Random(num, list_rock, board)
            covered = Cover(sublist_rock, board)
            for rock in sublist_rock:
                p = Point(rock, color, covered)
                points[rock] += p

        max_val = max(points.values())
        return [key for key, val in points.items() if val == max_val][0]