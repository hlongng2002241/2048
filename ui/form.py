from .ui_element import UiElement, Event
from .button import Button


class Form(UiElement):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def name(self) -> str:
        return "Form"

    def deselect_all_buttons(self, except_btn: Button = None):
        for child in self.children:
            if isinstance(child, Button) and child is not except_btn:
                child.set_state(child.NORMAL)
    
    def process_input(self, event: Event):
        for child in self.children:
            child.process_input(event)
