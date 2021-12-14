from .algorithm import Algorithm
from game.grid import Grid

class Expectimax(Algorithm):

    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

    def max_move(self, grid: Grid, depth: int) -> tuple[int, int]:
        """
        Visual and calculate next move for max player (move the board)
        Parameters
        ----------
            grid: Grid
                the current grid
            depth: int
                current depth

        Returns
        -------
            tuple of best_move and best_score
        """
        current_score = self.eval.evaluate(grid, True)

        if depth > self.max_depth or grid.is_terminal('max'):
            return -1, current_score

        moves = [1, 2, 3]
        best_move, max_score = -1, -self.eval.INFINITY

        for move in moves:
            save_board = list()
            if grid.can_move(move):
                grid.copy(grid.board, save_board)
                grid.move(move)
                _, score = self.expect_move(grid, depth + 1)
                grid.copy(save_board, grid.board)
                if score > max_score:
                    best_move, max_score = move, score

        return best_move, max_score

    def expect_move(self, grid: Grid, depth: int) -> tuple[int, int]:
        """
        Visual and calculate next move for expect player (random new tile)
        Parameters
        ----------
            grid: Grid
                the current grid
            depth: int
                current depth

        Returns
        -------
            tuple of best_move and best_score
        """
        current_score = self.eval.evaluate(grid, False)

        if depth > self.max_depth or grid.is_terminal('min'):
            return -1, current_score

        ROW, COLUMN = grid.ROW, grid.COLUMN
        RATE        = grid.RANDOM_4_RATE
        min_score   = self.eval.INFINITY

        for r in range(ROW):
            for c in range(COLUMN):
                if grid.board[r][c] == 0:
                    grid.board[r][c] = 2
                    _, score_2 = self.max_move(grid, depth + 1)
                    grid.board[r][c] = 4
                    _, score_4 = self.max_move(grid, depth + 1)
                    grid.board[r][c] = 0
                    min_score = min(min_score, score_2 * (1.0 - RATE) + score_4 * RATE)

        return -1, min_score
        # there is no need to find best move for min!!!

    def best_move(self, grid: Grid):
        move_direction, _ = self.max_move(grid, 1)

        if move_direction != -1:
            grid.move(move_direction, True)
        else:
            if grid.can_move_up():
                grid.move_up(True)
