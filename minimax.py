from .algorithm import Algorithm
from game.grid import Grid


class Minimax(Algorithm):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

    def max_move(self, grid: Grid, depth) -> tuple[int, int]:
        current_score = self.eval.evaluate(grid, True)
        if depth > self.max_depth or grid.is_terminal("max"):
            return -1, current_score

        dirs = [1, 2, 3]
        # moves is a list including possible moves for max
        # 0, 1, 2, 3
        max_score = - self.eval.INFINITY
        best_move = -1

        for move in dirs:
            save_board = list()
            if grid.can_move(move):
                temp_score = max_score
                grid.copy(grid.board, save_board)
                # copy from source to destination
                grid.move(move)
                max_score = max(max_score, self.min_move(grid, depth + 1)[1])
                grid.copy(save_board, grid.board)
                if max_score > temp_score and depth == 1:
                    best_move = move

        return best_move, max_score

    def min_move(self, grid: Grid, depth) -> tuple[int, int]:

        current_score = self.eval.evaluate(grid, False)

        if depth == self.max_depth or grid.is_terminal("max"):
            return -1, current_score

        min_score = self.eval.INFINITY
        ROW, COLUMN = grid.ROW, grid.COLUMN

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c] = 4
                    score_4 = self.max_move(grid, depth + 1)[1]
                    grid.board[r][c] = 2
                    score_2 = self.max_move(grid, depth + 1)[1]
                    grid.board[r][c] = 0
                    min_score = min(score_2, score_4, min_score, )

        return -1, min_score

    def best_move(self, grid: Grid):
        move_direction, _ = self.max_move(grid, 1)

        if move_direction != -1:
            grid.move(move_direction, True)
        #else:
            #if grid.can_move_up():
                #grid.move_up(True)
