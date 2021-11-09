class Board:
    def __init__(self, y=None, x=None):
        self.y = y
        self.x = x
        self.board = []

    def input(self):
        input_ = list(input()[:-1].split())
        self.y = int(input_[1])
        self.x = int(input_[2])
        _ = input()
        self.board = []
        for y in range(self.y):
            self.board.append(input().split()[1])