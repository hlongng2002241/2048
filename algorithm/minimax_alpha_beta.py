from game.grid import Grid
from .algorithm import Algorithm
from typing import Tuple


class MinimaxAlphaBeta(Algorithm):
    def __init__(self, max_depth) -> None:
        super().__init__(max_depth)

    def max_move(self, grid: Grid, alpha: int, beta: int, depth: int) -> Tuple[int, int]:
        current_score                   = self.eval.evaluate(grid, True)

        if depth == self.max_depth or grid.is_terminal('max'):
            return -1, current_score

        moves                           = [0, 1, 2, 3]
        best_move, max_score            = -1, -self.eval.INFINITY

        for move in moves:
            if grid.can_move(move):
                save_board = list()
                grid.copy(grid.board, save_board)
                grid.move(move)
                _, score = self.min_move(grid, alpha, beta, depth + 1)
                grid.copy(save_board, grid.board)

                if score > max_score:
                    best_move, max_score = move, score
                if alpha < max_score:
                    alpha = max_score
                if alpha >= beta:
                    return best_move, max_score

        return best_move, max_score

    def min_move(self, grid: Grid, alpha: int, beta: int, depth: int):

        current_score                   = self.eval.evaluate(grid, False)

        if depth == self.max_depth or grid.is_terminal('min'):
            return -1, current_score

        ROW, COLUMN                     = grid.ROW, grid.COLUMN
        RATE                            = grid.RANDOM_4_RATE
        min_score                       = self.eval.INFINITY

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    _, score_2          = self.max_move(grid, alpha, beta, depth + 1)
                    grid.board[r][c]    = 4
                    _, score_4          = self.max_move(grid, alpha, beta, depth + 1)
                    grid.board[r][c]    = 0
                    score               = min(score_2, score_4)
                    min_score           = min(min_score, score,score_2, score_4)

                    if score < min_score:
                        min_score       = score
                    if beta > min_score:
                        beta            = min_score
                    if alpha >= beta:
                        return -1, min_score

        return -1, min_score


    def best_move(self, grid: Grid) -> int:
        move_dir, _                     = self.max_move(grid, -self.eval.INFINITY, self.eval.INFINITY, 0)

        if move_dir != -1:
            grid.move(move_dir, True)
        #else:
            #grid.move_up(True)

        return move_dir
