from .algorithm import Algorithm
from game.grid import Grid
from typing import Tuple


class MixedExpectimax(Algorithm):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

        self.switch_sum                 = [1, 2, 4, 8, 16, 32, 64, 128, 256]

        self.cumulate_sum               = list()
        s                               = 0
        for x in self.switch_sum:
            s                          += x
            self.cumulate_sum.append(s)

    def infinity(self):
        return self.eval.INFINITY * self.cumulate_sum[self.max_depth]

    def max_move(self, grid: Grid, a: int, b: int, d: int) -> Tuple[int, int]:
        current_score                   = self.eval.evaluate(grid, True)

        if d >= self.max_depth or grid.is_terminal(who="max"):
            return (-1, current_score * self.switch_sum[d])

        dirs                            = [0, 1, 2, 3]
        best_move                       = -1
        best_score                      = -self.infinity()

        for direct in dirs:
            if grid.can_move(direct):
                save_board              = list()
                grid.copy(grid.board, save_board)
                grid.move(direct)
                _, score                = self.min_move(grid, a, b, d + 1)
                grid.copy(save_board, grid.board)

                score                  += current_score * self.switch_sum[d]

                if best_score < score:
                    best_score          = score
                    best_move           = direct

                if a < best_score:
                    a                   = best_score
                if b <= a:
                    return (best_move, best_score)

        return (best_move, best_score)

    def min_move(self, grid: Grid, a: int, b: int, d: int) -> Tuple[int, int]:
        current_score                   = self.eval.evaluate(grid, False)

        if d >= self.max_depth or grid.is_terminal(who="min"):
            return (-1, current_score * self.switch_sum[d])

        ROW, COLUMN                     = grid.ROW, grid.COLUMN
        RATE                            = grid.RANDOM_4_RATE

        best_score                      = self.infinity()

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:

                    grid.board[r][c]    = 2
                    _, score_2          = self.max_move(grid, a, b, d + 1)

                    grid.board[r][c]    = 4
                    _, score_4          = self.max_move(grid, a, b, d + 1)
                    
                    grid.board[r][c]    = 0

                    # Chance Nodes
                    score               = score_2 * (1.0 - RATE) + score_4 * RATE
                    score              += current_score * self.switch_sum[d]

                    if best_score > score:
                        best_score      = score

                    if b > best_score:
                        b               = best_score
                    if b <= a:
                        return (-1, best_score)

        return (-1, best_score)

    def best_move(self, grid: Grid) -> int:
        alpha                           = -self.infinity()
        beta                            = self.infinity()
        (move_idx, _)                   = self.max_move(grid, alpha, beta, 0)
        if move_idx != -1:
            grid.move(move_idx, True)

        return move_idx
        # else:
        #     if grid.can_move_up():
        #         grid.move_up(True)
