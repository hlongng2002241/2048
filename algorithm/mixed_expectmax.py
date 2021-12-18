from . algorithm import Algorithm
from game.grid import Grid


class MixedExpectimax(Algorithm):
    def __init__(self, depth : int = 5) -> None:
        super().__init__(depth)

        self.switch_sum                 = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        # self.PO_INF = self.eval.INFINITY * self.max_depth 
        # self.NE_INF = -self.eval.INFINITY * self.max_depth
        self.PO_INF = float("inf")
        self.NE_INF = float("-inf")


    def max_move(self, grid: Grid, a: int, b: int, d: int) -> tuple[int, int]:
        current_score                   = self.eval.evaluate(grid, True)

        if d >= self.max_depth or grid.is_terminal(who="max"):
            return (-1, current_score * self.switch_sum[d])
        
        dirs                            = [1,2,3]
        best_move                       = -1
        best_score                      = self.NE_INF

        for direct in dirs:
            if grid.can_move(direct):
                save_board = list()
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
                    break
        
        return (best_move, best_score)
    
    def min_move(self, grid: Grid, a: int, b: int, d: int) -> tuple[int, int]:
        current_score                   = self.eval.evaluate(grid, False)

        if d >= self.max_depth or grid.is_terminal(who="min"):
            return (-1, current_score * self.switch_sum[d])

        ROW, COLUMN                     = grid.ROW, grid.COLUMN
        RATE                            = grid.RANDOM_4_RATE

        best_score                      = self.PO_INF

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    _, score_2          = self.max_move(grid, a, b, d + 1)
                    grid.board[r][c]    = 4
                    _, score_4          = self.max_move(grid, a, b, d + 1)
                    grid.board[r][c]    = 0

                    score               = score_2 * (1.0 - RATE) + score_4 * RATE
                    score              += current_score * self.switch_sum[d]
                    if best_score > score:
                        best_score      = score
                    
                    if b > best_score:
                        b               = best_score
                    if b <= a:
                        break

        return (-1, best_score)

    def best_move(self, grid: Grid):
        alpha = self.NE_INF
        beta = self.PO_INF
        (move_idx, _) = self.max_move(grid, alpha, beta, 0)
        if move_idx != -1:
            grid.move(move_idx, True)
        else:
            if grid.can_move_up():
                grid.move_up(True)