from . algorithm import Algorithm
from game.grid import Grid


class Expectmax(Algorithm):
    def __init__(self, max_depth) -> None:
        super().__init__(max_depth=max_depth)

        self.__use_invert_sum   = False
        # self.__weights          = [0, 256, 128, 64, 32, 16, 8, 4, 2, 1]
        self.__weights          = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
        # self.__weights          = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def max_move(self, grid: Grid, depth) -> tuple[int, int]:
        """
        Visual and calculate next move for max player (move the board)
        Parameters
        ----------
            grid: Grid
                the current grid
            depth: int
                current depth
            alpha: int
                alpha value used for pruning
            beta: int 
                beta value used for pruning
        
        Returns
        -------
            tuple of best_move and best_score
        """
        current_score       = self.eval.evaluate(grid, True)
        
        if depth >= self.max_depth:
            if self.__use_invert_sum:
                return -1, current_score * self.__weights[depth]
            return -1, current_score

        if current_score == self.eval.GAME_OVER:
            return -1, current_score * (self.max_depth - depth + 1) 

        dirs                = [1, 2, 3]
        best_move           = -1
        best_score          = -self.eval.INFINITY * (self.max_depth if self.__use_invert_sum else 1)

        for direct in dirs:
            save_board      = list()
            if grid.can_move(direct):
                grid.copy(grid.board, save_board)
                grid.move(direct)
                _, score    = self.expect_move(grid, depth + 1)
                grid.copy(save_board, grid.board)

                score      += current_score * int(self.__use_invert_sum) * self.__weights[depth]
                
                if best_score < score:
                    best_score  = score
                    best_move   = direct

        return best_move, best_score

    def expect_move(self, grid: Grid, depth) -> tuple[int, int]:
        """
        Visual and calculate next move for expect player (random new tile)
        Parameters
        ----------
            grid: Grid
                the current grid
            depth: int
                current depth
            alpha: int
                alpha value used for pruning
            beta: int 
                beta value used for pruning
        
        Returns
        -------
            tuple of best_move and best_score
        """
        current_score       = self.eval.evaluate(grid, False)

        if depth >= self.max_depth:
            if self.__use_invert_sum:
                return -1, current_score * self.__weights[depth]
            return -1, current_score
        
        if current_score == self.eval.GAME_OVER:
            return -1, current_score * (self.max_depth - depth + 1)

        ROW, COLUMN         = grid.ROW, grid.COLUMN
        RATE                = grid.RANDOM_4_RATE

        best_score          = 0
        cnt                 = 0

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    _, score_2          = self.max_move(grid, depth + 1)
                    grid.board[r][c]    = 4
                    _, score_4          = self.max_move(grid, depth + 1)
                    grid.board[r][c]    = 0

                    score               = score_2 * (1.0 - RATE) + score_4 * RATE
                    score              += current_score * int(self.__use_invert_sum) * self.__weights[depth]

                    best_score         += score
                    cnt                += 1

        return -1, best_score // cnt

    def best_move(self, grid: Grid):
        move_idx, _ = self.max_move(grid, 0)
        
        if move_idx != -1:
            grid.move(move_idx, True)
        else:
            if grid.can_move_up():
                grid.move_up()