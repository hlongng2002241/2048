from . algorithm import Algorithm
from game.grid import Grid


class MinimaxAlphaBeta(Algorithm):
    def __init__(self, max_depth) -> None:
        super().__init__(max_depth=max_depth)

        self.__use_invert_sum   = True
        # self.__weights          = [0, 256, 128, 64, 32, 16, 8, 4, 2, 1]
        self.__weights          = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
        # self.__weights          = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def max_move(self, grid: Grid, depth, alpha: int, beta: int) -> int:
        current_score   = self.eval.evaluate(grid, True)
        
        if depth >= self.max_depth:
            if self.__use_invert_sum:
                return current_score * self.__weights[depth]
            return current_score

        if current_score == self.eval.GAME_OVER:
            return current_score * (self.max_depth - depth + 1) 

        moves           = [
            grid.move_down,
            grid.move_left,
            grid.move_right,
            # grid.move_up,
        ]
        
        can_moves       = [
            grid.can_move_down,
            grid.can_move_left,
            grid.can_move_right,
            # grid.can_move_up
        ]

        best_score      = -self.eval.INFINITY * (self.max_depth if self.__use_invert_sum else 1)

        for idx, move in enumerate(moves):
            save_board  = list()
            if can_moves[idx]():
                grid.copy(grid.board, save_board)
                move()
                score       = self.min_move(grid, depth + 1, alpha, beta)
                grid.copy(save_board, grid.board)

                score      += current_score * int(self.__use_invert_sum) * self.__weights[depth]
                
                if best_score < score:
                    best_score = score

                if alpha < best_score:
                    alpha = best_score
                if beta <= alpha:
                    return best_score

        return best_score

    def min_move(self, grid: Grid, depth, alpha: int, beta: int) -> int:
        current_score = self.eval.evaluate(grid, False)

        if depth >= self.max_depth:
            if self.__use_invert_sum:
                return current_score * self.__weights[depth]
            return current_score
        
        if current_score == self.eval.GAME_OVER:
            return current_score * (self.max_depth - depth + 1)

        ROW, COLUMN = grid.ROW, grid.COLUMN
        RATE        = grid.RANDOM_4_RATE

        best_score  = self.eval.INFINITY * (self.max_depth if self.__use_invert_sum else 1)

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    score_2             = self.max_move(grid, depth + 1, alpha, beta)
                    grid.board[r][c]    = 4
                    score_4             = self.max_move(grid, depth + 1, alpha, beta)
                    grid.board[r][c]    = 0

                    score               = score_2 * (1.0 - RATE) + score_4 * RATE
                    score              += current_score * int(self.__use_invert_sum) * self.__weights[depth]

                    if score < best_score:
                        best_score      = score

                    if beta > best_score:
                        beta            = best_score
                    if beta <= alpha:
                        return best_score
        return best_score

    def best_move(self, grid: Grid):
        moves       = [
            grid.move_down,
            grid.move_left,
            grid.move_right,
            # grid.move_up,
        ]

        can_moves   = [
            grid.can_move_down,
            grid.can_move_left,
            grid.can_move_right,
            # grid.can_move_up
        ]

        move_idx    = -1

        best_score  = -self.eval.INFINITY * (self.max_depth if self.__use_invert_sum else 1)

        for idx, move in enumerate(moves):
            save_board = list()
            if can_moves[idx]():
                grid.copy(grid.board, save_board)
                move()
                alpha       = -self.eval.INFINITY
                beta        = self.eval.INFINITY
                score       = self.min_move(grid, 1, alpha, beta)
                grid.copy(save_board, grid.board)

                if best_score < score:
                    best_score  = score
                    move_idx    = idx
        
        if move_idx != -1:
            moves[move_idx](True)
        else:
            if grid.can_move_up():
                grid.move_up()
