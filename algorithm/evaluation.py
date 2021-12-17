from types import GetSetDescriptorType
from pygame.constants import BLENDMODE_ADD
from game.grid import Grid
from copy import deepcopy

class Evaluation:   
    GAME_OVER           = -9999999999
    INFINITY            = 999999999999 

    BASIS_MATRIX        = [
        [10, 7, 4, 1],
        [100, 70, 40, 10],
        [1000, 700, 400, 100],
        [40000, 7000, 4000, 1000],
    ]

    WEIGHTS_MATRIX      = [
        [10, 7, 4, 1],
        [100, 70, 40, 10],
        [1000, 700, 400, 100],
        [40000, 7000, 4000, 1000],
    ]
    
                          
    def __init__(self) -> None:
        self.ROW            = 4
        self.COLUMN         = 4

    def evaluate(self, grid: Grid, is_movement: bool) -> int:
        """
        Evaluate the score of the board

        Parameters
        ----------
        grid: Grid

        is_movement: bool

        Returns
        -------
            evaluation: int
                return the evaluation value
        """
        if grid.is_terminal("max"):
            return self.GAME_OVER
        
        total = 0
        total += 2 * self.__evaluate_tiles_order(grid, is_movement)
        total += 1 * self.__evaluate_average(grid.board)
        total += 40 * self.__evaluate_potential_merge(grid.board)
        total += 30 * self.__evaluate_empty_tile(grid.board)
        return total
        
    def __evaluate_average(self, board: list) -> int:
        s, cnt          = 0, 0
        for row in board:
            for x in row:
                s      += x
                cnt    += 1 if x > 0 else 0
        
        return s // cnt
    
    def __evaluate_empty_tile(self, board: list) -> int:
        cnt             = 0
        for row in board:
            for x in row:
                cnt    += 1 if x == 0 else 0
        
        return cnt

    def __evaluate_potential_merge(self, board: list) -> int:
        used_in_R       = [[False for c in range(self.COLUMN)] for r in range(self.ROW)]
        used_in_C       = [[False for c in range(self.COLUMN)] for r in range(self.ROW)]
        cnt             = 0

        for r in range(self.ROW):
            for c in range(self.COLUMN):

                if r + 1 < self.ROW and board[r][c] == board[r + 1][c]:
                    if used_in_R[r][c] == False and used_in_R[r + 1][c] == False:
                        cnt                    += board[r][c] * 2
                        used_in_R[r][c]         = True
                        used_in_R[r + 1][c]     = True    
                    
                if c + 1 < self.COLUMN and board[r][c] == board[r][c + 1]:
                    if used_in_C[r][c] == False and used_in_C[r][c + 1] == False:
                        cnt                    += board[r][c] * 2
                        used_in_C[r][c]         = True
                        used_in_C[r][c + 1]     = True

        return cnt

    def set_up_weight_matrix(self, board: list, is_strict: bool):
        # store to a new array
        values = list()
        for row in board:
            for x in row:
                values.append(x)

        values.sort(reverse=True)    

        def is_good_enough(r: int, reverse: bool) -> bool:    
            if reverse:
                index_c = range(self.COLUMN - 1, -1, -1)
            else:
                index_c = range(self.COLUMN)

            strike = 0
            temp_values = deepcopy(values) 
            is_good = True
            
            for c in index_c:
                if temp_values[0] != 0:
                    if temp_values[0] == board[r][c]:
                        temp_values.pop(0)
                        strike += 1
                    elif is_strict is False and strike == 3 and temp_values[1] != 0 and temp_values[1] == board[r][c]:
                        temp_values.pop(1)
                    else:
                        is_good = False
                        break
                else:
                    is_good = False
                    break
            
            for c in index_c:
                values.remove(board[r][c])

            return is_good
        
        def set_row_matrix(r: int, reverse: bool):
            if reverse:
                index_c = range(self.COLUMN - 1, -1, -1)
            else:
                index_c = range(self.COLUMN)
            
            for i, c in enumerate(index_c):
                self.WEIGHTS_MATRIX[r][i] = self.BASIS_MATRIX[r][c]

        reverse = False
        is_good = False
        for r in range(self.ROW - 1, -1, -1):
            if is_good:
                reverse = not reverse
            
            set_row_matrix(r, reverse)
            is_good = is_good_enough(r, reverse)

    def __evaluate_tiles_order(self, grid: Grid, is_movement: bool) -> int:
        if is_movement:
            if (
                grid.can_move_left() is False
                and grid.can_move_right() is False
                and grid.can_move_down() is False
            ):
                return self.GAME_OVER
        
        cnt = 0
        self.set_up_weight_matrix(grid.board, False)

        for r in range(self.ROW):
            for c in range(self.COLUMN):
                cnt += grid.board[r][c] * self.WEIGHTS_MATRIX[r][c]

        return cnt
    
    
