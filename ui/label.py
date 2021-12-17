from src.utility import SharedFont
from .ui_element import UiElement, Event, Surface
import pygame.draw as pygame_draw
import pygame

class Label(UiElement):
    NORMAL_TEXT    = (0, 0, 0)
    
    def __init__(self, text: str, size, x, y, parent=None) -> None:
        super().__init__(parent=parent)
        self.position  = (x, y)
        self.text = text
        self.font_size = size

        self.redraw()

    def set_text(self, text: str):
        self.text = text
        self.redraw()

    def redraw(self):
        self.bg = SharedFont().get_font(self.font_size).render(self.text, True, self.NORMAL_TEXT)

            


    



        
