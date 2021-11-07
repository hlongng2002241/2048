## Note about class Grid 
    + If you do some actions with the grid's board, you can not bring the last state back, so if you want
    to do actions, copy the grid's board to another board, use copy() method in grid
    + This Grid has no animation

## Note about class Application:
    + if you want to switch the game mode, change PLAY_MODE to MODE_AI or MODE_HUMAN

## Name of variables, function and class
    + for normal variable:      use lower snake case: snake_case
    + for constant variable:    use upper snake case: SNAKE_CASE
    + for function:             same as normal variable
    + for class:                use capital camel case: CapitalCamelCase
    
tỉ lệ random ra 4 là 10%

class Evaluation:
    # đánh giá theo các tiêu chí
        + điểm trên số ô
        + đánh thứ tự các ô
            0   0   0   0
            0   0   0   0
            0   2   4   8
            128 64  32  16
        + đếm số ô trống
        + đếm số cặp ghép dc, ghép điểm càng to thì càng nhiều điểm

abstract class Algorithm:
    method best_move() => tính toán và quyết định nước đi

class Minimax(Algorithm):
    ...

class ...(Algorithm):
    ...
