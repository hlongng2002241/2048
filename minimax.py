from .algorithm import Algorithm
from game.grid import Grid


class Minimax(Algorithm):

    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

    def max_player(self, grid: Grid, depth):
        current_score = self.eval.evaluate(grid, True)

        if depth == self.max_depth or grid.is_terminal("max"):
            return current_score

        moves = grid.get_children('max')
        max_score = - self.eval.INFINITY
        best_move = moves[0]

        for move in moves:
            state = Grid(None)
            Grid.copy(grid.board, state.board)
            state.move(move)
            temp_score = max_score
            max_score = max(max_score, self.min_player(state, depth + 1))
            if max_score > temp_score and depth == 1:
                best_move = move
        if depth == 1:
            return (best_move, max_score)
        return max_score

    def min_player(self, grid: Grid, depth):
        current_score = self.eval.evaluate(grid, False)

        if depth == self.max_depth or grid.is_terminal("min"):
            return current_score

        moves = grid.get_children("min")
        min_score = self.eval.INFINITY

        for move in moves:
            state = Grid(None)
            Grid.copy(grid.board, state.board)
            state.place_tile(move[0], move[1], move[2])
            min_score = min(min_score, self.max_player(state, depth + 1))

        if depth == 1:
            return min_score
        return min_score
        # there is no need to find best move for min!!!

    def best_move(self, grid: Grid):
        grid.move(self.max_player(grid, 1)[0], True)