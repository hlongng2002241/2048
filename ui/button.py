import pygame
import pygame.draw as pygame_draw
from src.utility import SharedFont
from .ui_element import UiElement, Event, Surface


class Button(UiElement):
    BG_COLOR            = (250, 248, 240)
    NORMAL_TEXT         = (255, 255, 255)
    NORMAL_BOX          = (140, 122, 104)

    SELECTED_TEXT       = (255, 255, 255)
    SELECTED_BOX        = (160, 142, 124)
    
    TOGGLE_TEXT         = (255, 255, 255)
    TOGGLE_BOX          = (170, 142, 124)

    NORMAL              = 0
    TOGGLE              = 1
    SELECTED            = 2

    def __init__(self, text: str, size, x, y, w, h, parent=None) -> None:
        super().__init__(parent=parent)
        self.position   = (x, y)
        self.text       = text
        self.font_size  = size

        self.bg         = Surface((w, h))
        self.state      = self.NORMAL
        self.redraw()

        self.callback   = None

    def set_state(self, state):
        self.state      = state
        self.redraw()     
        return self

    def redraw(self):
        self.bg.fill(self.BG_COLOR)
        
        if self.state == self.NORMAL:
            box_color   = self.NORMAL_BOX
            text_color  = self.NORMAL_TEXT
        
        elif self.state == self.TOGGLE:
            box_color   = self.TOGGLE_BOX
            text_color  = self.TOGGLE_TEXT

        elif self.state == self.SELECTED:
            box_color   = self.SELECTED_BOX
            text_color  = self.SELECTED_TEXT

        w, h            = self.bg.get_size()
        pygame_draw.rect(self.bg, box_color, (0, 0, w, h), border_radius=5)

        text            = SharedFont().get_font(self.font_size).render(self.text, True, text_color)
        wt, ht          = text.get_size()
        x               = (w - wt) / 2
        y               = (h - ht) / 2
        self.bg.blit(text, (x, y, wt, ht))

    def process_input(self, event: Event):
        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            if self.global_bound().collidepoint(x, y):
                if self.state == self.NORMAL:
                    self.set_state(self.SELECTED)
            else:
                if self.state == self.SELECTED:
                    self.set_state(self.NORMAL)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.global_bound().collidepoint(x, y):
                if self.state != self.TOGGLE:
                    if self.parent is not None and isinstance(self.parent, UiElement) and self.parent.name() == "Form":
                        self.parent.deselect_all_buttons()
                    
                    self.set_state(self.TOGGLE)
                    if self.callback is not None:
                        self.callback()
            


    



        