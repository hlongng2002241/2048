# Classes for Algorithm
```
class Evaluation:
    method evaluate(board, ...)
    
    method evaluate_average() 
        => tính tổng các ô rồi chia cho số ô không trống
        => hệ số: 1.0

    method evaluate_empty_tiles() 
        => đếm số ô trống
        => hệ số 30.0

    method evaluate_potential_merge() 
        => đếm số cặp có thể ghép, cả chiều ngang lẫn dọc
        => tổng điểm là tổng của các cặp ghép dc
        => hệ số: 40.0
    
    method evaluate_tiles_order()
        => xét thứ tự sắp xếp của các ô trong bảng
        => có độ dài lớn nhất theo thứ tự là n
        => tổng điểm có thể là 2 ** n
        => hệ số: 5.0 
```


+ this abstract is important as other algorithm classes inherit from it
```
class Algorithm:
    method best_move(max_depth)
    method set_max_depth(max_depth)

```

```
class Minimax(Algorithm):
    ...
```

```
class MinimaxAlphaBeta(Algorithm):
    ...
```

```
class Expectmax(Algorithm):
    ...
```


# Classes for game
```
class Grid:
    method has_no_move(board)
    method random_new_tile()

    method draw_tile()
    method redraw()
    method draw(screen)

    method restart()
    method copy(src, des)
    
    method can_move_up()
    method can_move_down()
    method can_move_left()
    method can_move_right()

    method get_available_moves_for_max()
    method get_available_moves_for_min()
    method get_num_empty_tiles()
    method place_tile(row, column, tile)
    method get_children(who)

    method move_up()
    method move_down()
    method move_left()
    method move_right()
    method move(direction)
    method get_move_to(child)

    method is_terminal(who)
```

```
class Score:
    method reset_current_score()
    method add()
    method redraw()
    method draw_box()
    method draw()
```


+ This class saves all states from initial to final
```
class State:
    method load_file()
    method save_file()
    method load_next(board)
    method save_next(board)
```


# Classes for UI
+ We build UI structure the same as tree structure

+ this is a base class for all UI classes
```
class UiElement:
    method process_input(event)
    method update(dt)
    method draw(screen)

    => these 3 methods are the things you must concern about
```

```
class Button(UiElement):
    ...
```
    
```
class Form(UiElement):
    ...
```

```
class Label(UiElement):
    ...
```

# Classes for source
```
class Application:
    method run()
    method process_input()
    method update()
    method draw()
```

```
class GamePlay:
    ...
```

```
class Menu:
    ...
```