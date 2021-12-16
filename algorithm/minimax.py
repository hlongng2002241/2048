from . algorithm import Algorithm
from game.grid import Grid

PO_INF = float("inf")
NE_INF = float("-inf")

class Minimax(Algorithm):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)


    def max_move(self, grid: Grid, d):
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
                _, score        = self.min_move(grid, d)
                grid.copy(save_board, grid.board)
                if best_score < score:
                    best_score  = score 
                    best_move   = direct
        return (best_move, best_score)

    def min_move(self, grid:Grid, depth):

        if depth == 0 or grid.is_terminal(who="min"):
            return (None, self.eval.evaluate(grid, True))

        depth -= 1

        ROW, COLUMN         = grid.ROW, grid.COLUMN
        RATE                = grid.RANDOM_4_RATE

        min_score = PO_INF
        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    _, score_2          = self.max_move(grid, depth)
                    grid.board[r][c]    = 4
                    _, score_4          = self.max_move(grid, depth)
                    grid.board[r][c]    = 0

                    min_score = min(min_score, score_2, score_4)                  
        return -1, min_score

    
    def best_move(self, grid: Grid):
        move_idx, _         = self.max_move(grid, self.max_depth)
        grid.move(move_idx, True)