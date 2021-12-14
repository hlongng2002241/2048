from pygame import Surface
import pygame.draw as pygame_draw
from src.utility import SharedFont


class Score:
    BACKGROUND_COLOR            = (255, 255, 255)
    BOX_COLOR                   = (164, 218, 246)
    SCORE_COLOR                 = (255, 255, 255)
    TITLE_COLOR                 = (12, 55, 66)

    TITLE_SIZE                  = 16
    SCORE_SIZE                  = 24

    TILE_WIDTH                  = 90
    TILE_HEIGHT                 = 50
    BOX_SPACE                   = 5

    TOP_MARGIN                  = 0
    INSIDE_SPACE                = -5

    def __init__(self) -> None:
        self._current_score     = 0
        self._best_score        = 0
        self.titles             = ['SCORE', 'BEST']

        self.font_title         = SharedFont().get_font(self.TITLE_SIZE)
        self.font_title.bold    = True
        self.font_score         = SharedFont().get_font(self.SCORE_SIZE)
        self.font_score.bold    = True
        self.bg                 = Surface((self.TILE_WIDTH * 2 + self.BOX_SPACE, self.TILE_HEIGHT))
        self.position           = (0, 0)

        self.redraw()
    
    def reset_current_score(self):
        self._current_score     = 0
        self.draw_box(self._current_score, 0)

    def add(self, value: int):
        """
        Add value to current score

        Parameters
        ----------
            value: int
        """
        self._current_score    += value
        self.draw_box(self._current_score, 0)
        if self._best_score < self._current_score:
            self._best_score    = self._current_score
            self.draw_box(self._best_score, 1)
        
    def redraw(self):
        self.bg.fill(self.BACKGROUND_COLOR)
        self.draw_box(self._current_score, 0)
        self.draw_box(self._best_score, 1)

    def draw_box(self, score: int, idx: int):
        title                   = self.titles[idx]
        x                       = idx * (self.TILE_WIDTH + self.BOX_SPACE)
        y                       = 0
        pygame_draw.rect(self.bg, self.BOX_COLOR, (x, y, self.TILE_WIDTH, self.TILE_HEIGHT))

        y                      += self.TOP_MARGIN
        text                    = self.font_title.render(title, True, self.TITLE_COLOR)
        w, h                    = text.get_size()
        x_new                   = x + (self.TILE_WIDTH - w) / 2
        self.bg.blit(text, (x_new, y, w, h))

        y                      += self.font_title.get_linesize() + self.INSIDE_SPACE
        text                    = self.font_score.render(str(score), True, self.SCORE_COLOR)
        w, h                    = text.get_size()
        x_new                   = x + (self.TILE_WIDTH - w) / 2
        self.bg.blit(text, (x_new, y, w, h))
    
    def draw(self, screen):
        w, h                    = self.bg.get_size()
        x, y                    = self.position

        screen.blit(self.bg, (x, y, w, h))

    def current_score(self) -> int:
        return self._current_score





    




    