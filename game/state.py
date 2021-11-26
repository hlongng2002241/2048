from .grid import Grid


class State:
    def __init__(self, file_path: str) -> None:
        self.file_path  = file_path
        self.f          = None
        self.idx        = 0

    def load_file(self):
        self.f          = open(self.file_path, "r")
        self.idx        = 0

    def save_file(self):
        self.f          = open(self.file_path, "w")
        self.idx        = 0

    def save_next(self, board: list):
        self.f.write(str(self.idx) + "\n")
        self.idx       += 1
        for row in board:
            self.f.write(str(row) + "\n")

    def load_next(self, board: list):
        self.idx        = int(self.f.readline().split(max=1))
        for r in range(4):
            line        = eval(self.f.readline())
            for c in range(4):
                board[r][c] = line[c]
