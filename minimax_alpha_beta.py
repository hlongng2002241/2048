from game.grid import Grid
from sys import maxsize as MAX_INT
from .algorithm import Algorithm
from copy import deepcopy


class MinimaxAlphaBeta(Algorithm):

    def __init__(self, max_depth) -> None:
        super().__init__(max_depth)
        self.max_depth = max_depth

    def max_move(self, grid: Grid, alpha: int, beta: int, depth: int, max_depth: int):
        current_score = self.eval.evaluate(grid)

        if depth > max_depth  or grid.is_terminal(who='max'):
            return current_score

        moves = grid.get_children('max')
        best_move, max_score = moves[0], -MAX_INT

        for move in moves:
            state = Grid(current_score)
            state.board = deepcopy(grid.board)
            state.move(move)
            pre_score = max_score
            max_score = max(max_score, self.min_move(state, alpha, beta, depth + 1, max_depth))

            if max_score > pre_score and depth == 1:
                best_move = move
            if max_score >= beta:
                return max_score
            alpha = max(alpha, max_score)
        if depth == 1:
            return best_move, max_score
        return max_score

    def min_move(self, grid: Grid, alpha: int, beta: int, depth: int, max_depth: int):
        current_score = self.eval.evaluate(grid)

        moves = grid.get_children('min')
        min_score = MAX_INT

        for move in moves:
            state = Grid(current_score)
            state.board = deepcopy(grid.board)
            state.place_tile(move[0], move[1], move[2])
            min_score = min(min_score, self.max_move(state, alpha, beta, depth + 1, max_depth))

            if min_score <= alpha:
                return min_score
            beta = min(beta, min_score)
        if depth == 1:
            return None, min_score

        return min_score

    def best_move(self, grid: Grid):
        available_moves = grid.get_available_moves_for_max()
        best_move = available_moves[0] if available_moves else None
        max_score = -MAX_INT

        # Iterative deepening
        for d in range(1, self.max_depth):
            move, score = self.max_move(grid, -MAX_INT, MAX_INT, 1, d)
            if score > max_score:
                max_score, best_move = score, move

        grid.move(best_move)