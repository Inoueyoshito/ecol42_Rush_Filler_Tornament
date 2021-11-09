class Piece():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.piece = []

    def input(self):
        input_ = list(input().split())
        self.y = int(input_[1])
        self.x = int(input_[2].rstrip(":"))
        self.piece = []
        for y in range(self.y):
            self.piece.append(input())
