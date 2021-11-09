from demo_filler.demo.board import Board
from demo_filler.demo.piece import Piece


class Player:
    def __init__(self, player_num: int):
        self.player_num = player_num
        self.char = "O" if player_num == 1 else "X"
        self.new_char = "o" if player_num == 1 else "x"
        self.enemy_char = "X" if player_num == 1 else "O"
        self.enemy_new_char = "x" if player_num == 1 else "o"
        self.board = Board()
        self.piece = Piece()
        self.players = None
        self.enemies = None
        self.enemy_center = None
        self.player_center = None
        self.m_dist = None
        self.open_space = None

    def put_piece(self):
        self.m_dist = {}
        self.open_space = {}
        self.enemies = self.get_pos_list(lambda x: x in (self.enemy_new_char, self.enemy_char))
        self.players = self.get_pos_list(lambda x: x in (self.new_char, self.char))
        self.enemy_center = calc_center(self.enemies)
        self.player_center = calc_center(self.players)
        if self.solve():
            return
        print("0 0")

    def get_pos_list(self, judge_func) -> list:
        enemies = []
        for y in range(self.board.y):
            for x in range(self.board.x):
                if judge_func(self.board.board[y][x]):
                    enemies.append((x, y))
        return enemies

    def solve(self):
        board = self.board
        answers = []

        for y in range(board.y):
            for x in range(board.x):
                if self.is_inside(x, y) and not self.is_overlap(x, y):
                    answers.append((self.calc_piece_score(x, y), (x, y)))
        if answers:
            answers.sort(
                key=lambda x: (x[0][0][0], 4 - x[0][0][1]),
            )
            # print(answers)
            for scores, answer in answers:
                print(answer[1], answer[0])
                return True
            print(answers[-1][1], answers[-1][0])
            return True
        return False

    def is_overlap(self, top_left_x: int, top_left_y: int):
        piece = self.piece
        overlap_counter = 0

        for piece_y in range(piece.y):
            for piece_x in range(piece.x):
                if piece.piece[piece_y][piece_x] != "*":
                    continue
                if (top_left_x + piece_x, top_left_y + piece_y) in self.enemies:
                    return True
                if (top_left_x + piece_x, top_left_y + piece_y) in self.players:
                    overlap_counter += 1

        if overlap_counter != 1:
            return True
        return False

    def is_inside(self, top_left_x: int, top_left_y: int) -> bool:
        piece = self.piece
        board = self.board

        if (top_left_x < 0) or (top_left_y < 0):
            return False
        if ((top_left_x + piece.x) > board.x) or ((top_left_y + piece.y) > board.y):
            return False
        return True

    def calc_piece_score(self, x: int, y: int) -> list:
        scores = []
        piece = self.piece.piece
        board = self.board.board

        distance = 0
        for piece_y in range(self.piece.y):
            for piece_x in range(self.piece.x):
                if piece[piece_y][piece_x] != "*":
                    continue
                if board[y + piece_y][x + piece_x] != ".":
                    continue
                # distance += self.calc_manhattan_dist(x + piece_x, y + piece_y)
                distance = self.calc_manhattan_dist(x + piece_x, y + piece_y)
                space = self.calc_open_spaces(x + piece_x, y + piece_y)
                scores.append((distance, space))
        scores.sort()
        return scores

    def calc_manhattan_dist(self, x: int, y: int) -> int:
        distance = self.m_dist.get((x, y))
        if distance is None:
            # it is not actually distance
            # distance = abs(y - self.enemy_center[1]) + abs(x - self.enemy_center[0])
            distance = min([abs(y - enemy[1]) + abs(x - enemy[0]) for enemy in self.enemies])
            # distance -= abs(y - self.player_center[1]) + abs(x - self.player_center[0])

            self.m_dist[(x, y)] = distance
        return distance

    def calc_open_spaces(self, x: int, y: int):
        space = self.open_space.get((x, y))
        if space is not None:
            return space
        space = 0
        if y != 0 and self.board.board[y - 1][x] == ".":
            space += 1
        if y != self.board.y - 1 and self.board.board[y + 1][x] == ".":
            space += 1
        if x != 0 and self.board.board[y][x - 1] == ".":
            space += 1
        if x != self.board.x - 1 and self.board.board[y][x + 1] == ".":
            space += 1
        self.open_space[(x, y)] = space
        return space


def calc_center(pos: list) -> tuple:
    num = len(pos)
    center_x = sum(p[0] for p in pos) // num
    center_y = sum(p[1] for p in pos) // num
    return center_x, center_y
