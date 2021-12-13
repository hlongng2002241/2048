# UI for 2048 AI
## Intro
+ This UI is used only supported with 3 base elements: button, form and label, in which button is selectable while the rest are not

## Structure of UI
+ We design this quick UI base on tree structure
    ```
    Form
    |
    +--- Button
    |
    +--- Button
    |
    +--- Label
    |
    +--- Form
    |    |
    |    +--- Label
    |    |
    |    +--- Button
    |
    +--- Button
        
    ```

+ the tree root should be a Form
+ all `position` in element is RELATIVE position
+ 
## Basis elements
+ UI_Element:
  + contains basis abstract methods for single element, such as:
    + process_input(event)
    + update(dt)
      + update_current()
      + update_children
    + draw(screen)
      + draw_current()
      + draw_children()
    + name()
    + global_position()
    + global_bounds()
  + with abstract methods, we recommend to use update_current(), update_children(), draw_current(), draw_children() instead of directly using update() and draw(). BUT, if you have to, please read the methods' structure

+ Button:
  + In button, you should concern about its `callback` attribute. The callback must be the function pointer with no argument.
  + For example:
    ```python
    def btn_callback():
        ...
    
    btn = Button(...)
    btn.callback = btn_callback()
    ```
  + `callback` will be activated when mouse button CLICK, not PRESS or RELEASE
  + you can use `chain settings` like this:
    ```python
    Button("Human", font_size, 180, 34, 175, 40, form_mode).set_state(Button.TOGGLE).callback = lambda: self.gameplay.set_play_mode(self.gameplay.MODE_HUMAN)
    ```
  + if you want to change button's color, you should redraw() it 
  
+ Label:
  + pretty easy to use
  + no arrangement

+ Form:
  + with deselected_all_children() => all buttons will be deselected