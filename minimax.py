from grid import Grid
from sys import maxsize as MAX_INT
from algorithm import Algorithm

class Minimax_ab(Algorithm):

    def __init__(self, max_depth) -> None:
        super().__init__()

    def maximize(self, grid: Grid, alpha: int, beta: int, depth: int):
        # d is the maximum allowed depth
        # maxChild is the children of the current grid object (in the minimax algorithm tree) that maximizes the utility, and maxUtility is the utility value of maxChild game grid
        # maxUtility variable will hold the maximum utility of a node encountered so far. At the beginning of the function, we don’t know any utility value, so we consider the maximum so far to be a number smaller than anything a utility value can be. I chose -1
        maxChild, maxUtility = None, -1
        # checking if the current grid is a terminal node or if we reached the maximum depth. If so, we return None as the maxChild and evaluate the current grid’s utility
        if depth == 0 or grid.has_no_move():
            return None, self.eval.evaluate(grid)
        depth -= 1
        # the child variable in the for loop is a move direction code that is used to make this move
        for child in grid.get_children(who='max'):
            # In each iteration we make a copy of the current game grid and make a move in one of the available moves
            grid = Grid()
            grid.move(child)
            # let Min do his move through the minimize() function and get back from this function the utility of the current iteration’s child grid
            _, utility = self.minimize(grid, alpha, beta, depth)
            if utility > maxUtility:
                maxChild, MaxUtility = grid, utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = MaxUtility

        return maxChild, maxUtility

    def minimize(self, grid: Grid, alpha: int, beta: int, depth: int):
        minChild, minUtility = None, MAX_INT

        if depth == 0 or grid.is_terminal(who='min'):
            return None, self.eval.evaluate(grid)
        depth -= 1

        for child in grid.get_children(who='min'):
            grid = Grid()
            grid.place_tile(child[0], child[1], child[2])
            _, utility = self.maximize(grid, alpha, beta, depth)
            if utility < minUtility:
                minChild, minUtility = grid, utility
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility

        return minChild, minUtility

    # The get_best_move() function calls maximize() and returns the code of the move that we have to take to maximize our score/utility
    def get_best_move(self, grid, depth: int = 5):
        child, _ = self.maximize(Grid(), -1, MAX_INT, depth)
        return grid.get_move_to(child)