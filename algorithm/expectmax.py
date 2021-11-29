from . algorithm import Algorithm, Point
from game.grid import Grid


class Expectmax(Algorithm):
    def __init__(self, max_depth) -> None:
        super().__init__(max_depth=max_depth)

        self.use_sum   = False
        self.four_dir  = False

    def max_move(self, grid: Grid, depth) -> Point:
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

        INF         = self.eval.INFINITY * (self.max_depth if self.use_sum else 1)
        best_score  = Point([-INF], self.eval.num_eval)

        for move in moves:
            save_board = list()
            grid.copy(grid.board, save_board)
            if move():
                score       = self.expecti_move(grid, depth + 1)
                grid.copy(save_board, grid.board)
                
                score       = score + current_score * (1 if self.use_sum else 0)
                if best_score < score:
                    best_score = score.copy()

        return best_score

    def expecti_move(self, grid: Grid, depth) -> Point:
        current_score = self.eval.evaluate(grid.board, False)

        if current_score.points[0] == self.eval.GAME_OVER:
            return current_score

        if depth >=self.max_depth:
            return current_score

        ROW, COLUMN = grid.ROW, grid.COLUMN
        RATE        = grid.RANDOM_4_RATE

        best_score  = Point([0 for i in range(self.eval.num_eval)])
        cnt         = 0

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c]    = 2
                    score_2             = self.max_move(grid, depth + 1)
                    grid.board[r][c]    = 4
                    score_4             = self.max_move(grid, depth + 1)
                    grid.board[r][c]    = 0

                    score               = score_2 * (1.0 - RATE) + score_4 * RATE
                    score               = score + current_score * (1 if self.use_sum else 0)

                    best_score          = best_score + score
                    cnt                += 1
                    
        return best_score * (1 / cnt)

    def best_move(self, grid: Grid):
        moves       = [
            grid.move_down,
            grid.move_left,
            grid.move_right,
            # grid.move_up,
        ]
        if self.four_dir:
            moves.append(grid.move_up)
        
        move_idx    = -1
        INF         = self.eval.INFINITY * (self.max_depth if self.use_sum else 1)

        best_score  = Point([-INF], self.eval.num_eval)

        for idx, move in enumerate(moves):
            save_board = list()
            grid.copy(grid.board, save_board)
            if move():
                score       = self.expecti_move(grid, 1)
                grid.copy(save_board, grid.board)

                if best_score < score:
                    best_score  = score.copy()
                    move_idx    = idx

        if move_idx == -1:
            grid.move_up()
        else:
            moves[move_idx]()
