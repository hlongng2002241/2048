from game.grid import Grid
from .algorithm import Algorithm


class MinimaxAlphaBeta(Algorithm):

    def __init__(self, max_depth) -> None:
        super().__init__(max_depth)

    def max_move(self, grid: Grid, alpha: int, beta: int, depth: int):
        current_score = self.eval.evaluate(grid, True)

        if depth > self.max_depth or grid.is_terminal(who='max'):
            return current_score

        moves = grid.get_children('max')
        best_move, max_score = moves[0], - self.eval.INFINITY

        for move in moves:
            state = Grid(None)
            Grid.copy(grid.board, state.board)
            state.move(move)
            pre_score = max_score
            max_score = max(max_score, self.exp_move(state, alpha, beta, depth + 1))

            if max_score > pre_score and depth == 1:
                best_move = move
            if max_score >= beta:
                return max_score
            alpha = max(alpha, max_score)
        if depth == 1:
            return best_move, max_score
        return max_score

    def exp_move(self, grid: Grid, alpha: int, beta: int, depth: int):
        current_score = self.eval.evaluate(grid, True)
        moves = grid.get_children('min')
        min_score = self.eval.INFINITY

        for move in moves:
            state = Grid(None)
            Grid.copy(grid.board, state.board)
            state.place_tile(move[0], move[1], move[2])
            min_score = min(min_score, self.max_move(state, alpha, beta, depth + 1))

            if min_score <= alpha:
                return min_score
            beta = min(beta, min_score)
        if depth == 1:
            return None, min_score

        return min_score

    def best_move(self, grid: Grid):
        best_move, max_score = self.max_move(grid, - self.eval.INFINITY, self.eval.INFINITY, 1)
        grid.move(best_move, True)
