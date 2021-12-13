from pygame import Surface
from pygame.event import Event
import pygame

class UiElement:
    def __init__(self, parent=None) -> None:
        """
        Parameters
        ----------
            parent: default=None
                parent must has attribute "position" as tuple(int, int)
        """
        self.position   = (0, 0)
        self.bg         = Surface((0, 0))
        self.parent     = parent
        self.children   = list()

        if parent is not None and isinstance(parent, UiElement):
            parent.children.append(self)

    def name(self) -> str:
        return "UiElement"

    def global_position(self) -> tuple[int,int]:
        x, y = 0, 0
        ele = self
        while ele != None:
            x += ele.position[0]
            y += ele.position[1]
            
            if hasattr(ele, "parent") is False:
                break
            ele = ele.parent
        return (x, y)

    def global_bound(self) -> pygame.Rect:
        x, y = self.global_position()
        w, h = self.bg.get_size()
        return pygame.Rect(x, y, w, h)

    def process_input(self, event: Event):
        pass

    def update(self, dt):
        self.update_current(dt)
        self.update_children(dt)

    def update_current(self, dt):
        pass

    def update_children(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, screen: Surface):
        self.draw_current(screen)
        self.draw_children(screen)

    def draw_current(self, screen: Surface):
        x, y = self.global_position()
        w, h = self.bg.get_size()
        screen.blit(self.bg, (x, y, w, h))

    def draw_children(self, screen: Surface):
        for child in self.children:
            child.draw(screen)

    

        
