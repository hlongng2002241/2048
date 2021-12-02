from . algorithm import Algorithm
from game.grid import Grid


class Minimax(Algorithm):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

    # def minimax(self, grid: Grid, depth, is_max_player):        
    #     current_score = grid.board.evaluate()
    #     # function evaluate has not been written yet
    #     if depth == 0 or grid.is_terminal("max"):
    #         return current_score
    #     if is_max_player:
    #         point = - infinity
    #         for child in get_children("max"):
    #         # get children max return list of possible
    #         # moves(including 0,1,2,3)
    #             temp_point = minimax(""child nodes"")

    def max_player(self, grid: Grid, depth):
        current_score = self.eval.evaluate(grid, True)
        if depth == self.max_depth or grid.is_terminal("max"):
            return current_score
        moves = grid.get_children('max')
        #moves is a list including possible moves for max 
        #0,1,2,3
        max_score = - self.eval.INFINITY
        best_move = moves[0]
        for move in moves:
            state = Grid(None)
            # create an instant for Grid 
            Grid.copy(grid.board, state.board)
            # copy from source to destination
            state.move(move)
            temp_score = max_score
            max_score = max(max_score, self.min_player(state, depth + 1))
            if max_score > temp_score and depth == 1:
                best_move = move
        if depth == 1:
            return best_move, max_score
        return max_score
            
    def min_player(self, grid:Grid, depth):
        current_score = self.eval.evaluate(grid, False)
        if depth == self.max_depth or grid.is_terminal("max"):
            return current_score
        moves = grid.get_children("min")
        # get_children return a list of triplets (i,j, and 2/4)
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
        # function best move set a optimal move for the current states (not just tell)
        # the move only
        grid.move(self.max_player(grid, 1)[0], True)


    

            
        