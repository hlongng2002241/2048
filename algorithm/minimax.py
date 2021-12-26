from .algorithm import Algorithm
from game.grid import Grid


class Minimax(Algorithm):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

    def max_player(self, grid: Grid, depth):
        current_score                   = self.eval.evaluate(grid, True)

        if depth == self.max_depth or grid.is_terminal("max"):
            return -1, current_score

        dirs                            = [0, 1, 2, 3]
        # moves is a list including possible moves for max
        # 0, 1, 2, 3
        max_score                       = - self.eval.INFINITY
        best_move                       = -1

        for move in dirs:
            if grid.can_move(move):
                save_board              = list()
                temp_score              = max_score
                grid.copy(grid.board, save_board)
                # copy from source to destination
                grid.move(move)
                max_score = max(max_score, self.min_player(grid, depth + 1)[1])
                grid.copy(save_board, grid.board)
                if max_score > temp_score:
                    best_move           = move

        return best_move, max_score

    def min_player(self, grid: Grid, depth):
        current_score                   = self.eval.evaluate(grid, False)

        if depth == self.max_depth or grid.is_terminal("min"):
            return -1, current_score

        min_score                       = self.eval.INFINITY
        ROW, COLUMN                     = grid.ROW, grid.COLUMN

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 4
                    score_4             = self.max_player(grid, depth + 1)[1]
                    grid.board[r][c]    = 2
                    score_2             = self.max_player(grid, depth + 1)[1]
                    grid.board[r][c]    = 0
                    min_score           = min(min_score, score_2, score_4)

        return -1, min_score

    def best_move(self, grid: Grid) -> int:
        # function best move set a optimal move for the current states (not just tell)
        # the move only
        move_idx, _                     = self.max_player(grid, 0)
        if move_idx != -1:
            grid.move(move_idx, True)

        return move_idx
        # else:
        #     if grid.can_move_up():
        #         grid.move_up(True)
