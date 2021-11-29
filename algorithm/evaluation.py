from game.grid import Grid
from . point import Point
import math

class Evaluation:
    BONUS               = 200
    MODEL_BONUS         = 400       
    MODEL_BAD_CASE      = -10000      
    GAME_OVER           = -999999999  
    INFINITY            = 99999999999 
                          
    def __init__(self) -> None:
        self.ROW        = 4
        self.COLUMN     = 4
        self.num_eval   = 1

    def evaluate(self, board: list, is_movement: bool) -> Point:
        if Grid.has_no_move(None, board):
            return Point([self.GAME_OVER], self.num_eval)
        
        return Point([
            # self.evaluate_tiles_order(board, is_movement),
            self.evaluate_average(board),
            # self.evaluate_potential_merge(board),
            # self.evaluate_empty_tile(board),
        ])
        
    def evaluate_average(self, board: list) -> int:
        s, cnt          = 0, 0
        for row in board:
            for x in row:
                s      += x
                cnt    += 1 if x > 0 else 0
        
        return s // cnt
    
    def evaluate_empty_tile(self, board: list) -> int:
        cnt             = 0
        for row in board:
            for x in row:
                cnt    += 1 if x == 0 else 0
        
        return cnt * self.BONUS

    def evaluate_potential_merge(self, board: list) -> int:
        used_in_R       = [[False for c in range(self.COLUMN)] for r in range(self.ROW)]
        used_in_C       = [[False for c in range(self.COLUMN)] for r in range(self.ROW)]
        cnt             = 0

        for r in range(self.ROW):
            for c in range(self.COLUMN):

                if r + 1 < self.ROW and board[r][c] == board[r + 1][c]:
                    if used_in_R[r][c] == False and used_in_R[r + 1][c] == False:
                        cnt                    += 1
                        used_in_R[r][c]         = True
                        used_in_R[r + 1][c]     = True    
                    
                if c + 1 < self.COLUMN and board[r][c] == board[r][c + 1]:
                    if used_in_C[r][c] == False and used_in_C[r][c + 1] == False:
                        cnt                    += 1
                        used_in_C[r][c]         = True
                        used_in_C[r][c + 1]     = True

        return cnt * self.BONUS

    def evaluate_tiles_order(self, board: list, is_movement: bool) -> int:
        """
        This function is used for case: all biggest tile is located on bottom line
        """
        tmp                 = list()
        for row in board:
            for x in row:
                tmp.append(x)
        
        tmp                 = sorted(tmp, reverse=True)

        current_r           = self.ROW - 1
        current_c           = -1
        dc                  = 0
        score               = 0

        if board[current_r][0] == tmp[0]:
            current_c       = 0
            dc              = 1

        if board[current_r][self.COLUMN - 1] == tmp[0]:
            current_c       = self.COLUMN - 1
            dc              = -1
        
        if current_c == -1:
            return -2048


        score              += self.MODEL_BONUS * max(5, math.log(tmp[0]))
        idx                 = 0
        while True:
            idx += 1
            if tmp[idx] == 0:
                break

            current_c      += dc

            if current_c < 0:
                current_r  -= 1
                current_c   = 0 
                dc          = 1
            
            if current_c >= self.COLUMN:
                current_r  -= 1
                current_c   = self.COLUMN - 1
                dc          = -1
            
            if current_r < 0:
                break
            
            if tmp[idx] != board[current_r][current_c]:
                break

        
        for i in range(idx):
            score += self.MODEL_BONUS * math.log(tmp[i], 2)

        # detect special case =============================
        if is_movement is False:
            BLANK   = -1
            FULL    = 1
            state   = [0 for _ in range(self.ROW)]

            for r in range(self.ROW):
                is_blank = True
                is_full  = True
                for c in range(self.COLUMN):
                    if board[r][c] != 0:
                        is_blank    = False
                        break
                
                    if board[r][c] == 0:
                        is_full     = False
                        break
                
                if is_full:
                    state[r] = FULL

                if is_blank:
                    state[r] = BLANK

            if (
                    state == [BLANK, BLANK, BLANK, FULL] 
                or  state == [BLANK, BLANK, FULL,  FULL] 
                or  state == [BLANK, FULL,  FULL,  FULL] 
            ):
                score += self.MODEL_BAD_CASE
        
        return score
