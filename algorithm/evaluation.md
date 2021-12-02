# Evaluation:
## Overview:
+ Evaluation (or heuristic) is the task where we calculate score for the board. This score is not the same as the score the game uses, this score can be considered to be the signal that makes the AI knows how good the board is to make decision for the next move.
+ There are lots of ways to achieve this and here is our strategy:
  + The average score of none empty tiles
  + The number of empty tiles
  + The location of the largest tile (here we give 2048 score for the right location)
  + The number of possible merges
  + The structure of the board or we call it monotonicity of the board

  + `Note`: Here we use the weight for each evaluation: <br/>
        1, 30, 1, 40, 2 <br/>
        with respect to the same order as above <br/>

## Details:
### Let's start with the first evaluation: Average value of none empty tile:
+ Like its name, it is pretty simple to understand.
+ Here is the code:
    ```
    def _evaluate_average(self, board: list) -> int:
        s, cnt          = 0, 0
        for row in board:
            for x in row:
                s      += x
                cnt    += 1 if x > 0 else 0
        
        return s // cnt
    ```

### Next is the easiest evaluation: Number of empty tiles:
    ```
    def _evaluate_empty_tile(self, board: list) -> int:
        cnt             = 0
        for row in board:
            for x in row:
                cnt    += 1 if x == 0 else 0
        
        return cnt
    ```

### The following evaluation is: Location of the largest tile:
+ We set this tile to the left bottom conner of the board
    ```
    def _evaluate_biggest_tile(self, board: list) -> int:
        mx = 0
        for row in board:
            for x in row:
                mx = max(mx, x)
        
        if board[3][0] == mx:
            return mx * self.WEIGHTS_MATRIX[0][3][0]
        return self.GAME_OVER
    ```

### After that, we get the evaluation which is a bit harder to handle: Number of possible merge:
+ The idea is really easy:
  + First, we initialize 2 list to mark down the tiles which are counted 
  + Second, we search for two tiles which are adjacent and have the same tile
    + If those are in the same row, check if they are used or not
    + If none of they are used, increase `cnt` to the sum of their values
    + Same with column

    ```
    def _evaluate_potential_merge(self, board: list) -> int:
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
    ```

### Finally we handle the hardest evaluation: Monotonicity of the board
+ Start with the weight matrix:
    ```
        [1, 4, 7, 10],
        [100, 70, 40, 10],
        [100, 400, 700, 1000],
        [30000, 7000, 4000, 1000],
    ```
+ Here is one of four matrices we use and this is the final matrix
+ We match each tile in the board with a single score to generate the monotonicity of the board. Here you can see the location values is decrease in a particular direction
+ Also, to choose the suitable matrix (as I said above that we have 4 matrix), we determine base on the tiles in each row
+ For example:
  + if the last row is not good, we use matrix number 0
  + if the last row is good enough, we use matrix number 1
  + if the last and second last rows are good enough, we use matrix number 2
  + and so on ...
+ `Note`: `good enough` is just a way of speaking
+ Here is the code to choose matrix index:
    ```
    def _choose_weight_index(self, board: list) -> int:
        """
        Choose the suitable weight matrix for the evaluation
        This bases on the playing strategy of the AI
            It check from the last row to the first one
            If the last row is not good, use 0
            If the last row is good enough, use 1
            If the last row and the second last row is good enough, use 2
            And so on ...
        """
    ```
    and the method to check if the row is good enough or not:
    ```
    def check_row(r, reverse) -> bool:
        ...
    ```
  + You can see more in the source code

+ Finally is the code for evaluation idea:
    ```
    def _evaluate_tiles_order(self, grid: Grid, is_movement: bool) -> int:
        if is_movement:
            if (
                grid.can_move_left() is False
                and grid.can_move_right() is False
                and grid.can_move_down() is False
            ):
                return self.GAME_OVER
        
        cnt = 0
        idx = self._choose_weight_index(grid.board)
        
        for r in range(self.ROW):
            for c in range(self.COLUMN):
                cnt += grid.board[r][c] * self.WEIGHTS_MATRIX[idx][r][c]

        return cnt
    ```
+ Also, we avoid the moving up as the structure of the board may be broken