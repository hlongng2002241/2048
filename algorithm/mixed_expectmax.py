from . algorithm import Algorithm
from game.grid import Grid
from typing import Tuple

PO_INF = float("inf")
NE_INF = float("-inf")

class Mixed_Expectmax_Minimax(Algorithm):
    def __init__(self, depth : int = 5) -> None:
        super().__init__(depth)

    def max_move(self, grid: Grid, a: int, b: int, d: int) -> Tuple[int, int]:
        if d == 0 or grid.is_terminal(who="max"):
            return (None, self.eval.evaluate(grid, True))
        
        d -= 1
        
        dirs = [0,1,2,3]
        best_move = -1
        best_score = NE_INF


        for direct in dirs:
            save_board = list()
            if grid.can_move(direct):
                grid.copy(grid.board, save_board)
                grid.move(direct)
                _, score        = self.min_move(grid, a, b, d)
                grid.copy(save_board, grid.board)
                if best_score < score:
                    best_score  = score 
                    best_move   = direct
                if a < best_score:
                    a               = best_score
                if b <= best_score:
                    break
        return (best_move, best_score)
    
    def min_move(self, grid: Grid, a: int, b: int, d: int) -> Tuple[int, int]:
        if d == 0 or grid.is_terminal(who="min"):
            return (None, self.eval.evaluate(grid, True))

        d -= 1
        
        ROW, COLUMN         = grid.ROW, grid.COLUMN
        RATE                = grid.RANDOM_4_RATE

        best_score = PO_INF

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    _, score_2          = self.max_move(grid, a, b, d)
                    grid.board[r][c]    = 4
                    _, score_4          = self.max_move(grid, a, b, d)
                    grid.board[r][c]    = 0

                    score               = score_2 * (1.0 - RATE) + score_4 * RATE

                    if best_score > score:
                        best_score      = score
                    if a <= best_score:
                        break
                    if b > best_score:
                        b               = best_score
                    
        return (-1, best_score)

    def best_move(self, grid: Grid, depth: int = 5) -> int:
        (move_idx, _) = self.max_move(grid, NE_INF, PO_INF, depth)
        grid.move(move_idx, True)