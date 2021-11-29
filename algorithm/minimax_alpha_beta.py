from . algorithm import Algorithm, Point
from game.grid import Grid


class MinimaxAlphaBeta(Algorithm):
    def __init__(self, max_depth) -> None:
        super().__init__(max_depth=max_depth)

        self.use_sum   = False
        self.four_dir  = False

    def max_move(self, grid: Grid, depth, alpha: Point=None, beta: Point=None) -> Point:
        current_score = self.eval.evaluate(grid.board, True)
        
        if current_score.points[0] == self.eval.GAME_OVER:
            return current_score

        if depth >=self.max_depth:
            return current_score

        moves       = [
            grid.move_down,
            grid.move_left,
            grid.move_right,
            # grid.move_up,
        ]
        if self.four_dir:
            moves.append(grid.move_up)
        
        can_moves   = [
            grid.can_move_down,
            grid.can_move_left,
            grid.can_move_right,
            grid.can_move_up
        ]

        INF         = self.eval.INFINITY * (self.max_depth if self.use_sum else 1)
        best_score  = Point([-INF], self.eval.num_eval)

        for idx, move in enumerate(moves):
            save_board = list()
            if can_moves[idx]():
                grid.copy(grid.board, save_board)
                move()
                score       = self.min_move(grid, depth + 1, alpha.copy(), beta.copy())
                grid.copy(save_board, grid.board)
                
                score       = score + current_score * (1 if self.use_sum else 0)
                if best_score < score:
                    best_score = score.copy()

                if alpha is not None:
                    if alpha < best_score:
                        alpha = best_score.copy() 
                    if beta is not None and beta <= alpha:
                        return best_score

        return best_score

    def min_move(self, grid: Grid, depth, alpha: Point=None, beta: Point=None) -> Point:
        current_score = self.eval.evaluate(grid.board, False)

        if current_score.points[0] == self.eval.GAME_OVER:
            return current_score

        if depth >= self.max_depth:
            return current_score

        ROW, COLUMN = grid.ROW, grid.COLUMN
        RATE        = grid.RANDOM_4_RATE

        INF         = self.eval.INFINITY * (self.max_depth if self.use_sum else 1)
        best_score  = Point([INF for i in range(self.eval.num_eval)])

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    score_2             = self.max_move(grid, depth + 1, alpha.copy(), beta.copy())
                    grid.board[r][c]    = 4
                    score_4             = self.max_move(grid, depth + 1, alpha.copy(), beta.copy())
                    grid.board[r][c]    = 0

                    score               = score_2 * (1.0 - RATE) + score_4 * RATE
                    score               = score + current_score * (1 if self.use_sum else 0)

                    if score < best_score:
                        best_score      = score.copy()

                    if beta is not None:
                        if beta > best_score:
                            beta        = best_score.copy()
                        if alpha is not None and beta <= alpha:
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
            grid.can_move_up
        ]
        
        if self.four_dir:
            moves.append(grid.move_up)

        move_idx    = -1
        INF         = self.eval.INFINITY * (self.max_depth if self.use_sum else 1)

        best_score  = Point([-INF], self.eval.num_eval)

        for idx, move in enumerate(moves):
            save_board = list()
            if can_moves[idx]():
                grid.copy(grid.board, save_board)
                move()
                alpha       = Point([-INF], self.eval.num_eval)
                beta        = Point([INF], self.eval.num_eval)
                score       = self.min_move(grid, 1, alpha, beta)
                grid.copy(save_board, grid.board)

                if best_score < score:
                    best_score  = score.copy()
                    move_idx    = idx
        
        if move_idx == -1:
            grid.move_up()
        else:
            moves[move_idx](True)
