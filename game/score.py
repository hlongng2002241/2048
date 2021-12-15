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
        self.titles             = ['SCORE', 'BEST', 'MOVES']

        self.font_title         = SharedFont().get_font(self.TITLE_SIZE)
        self.font_title.bold    = True
        self.font_score         = SharedFont().get_font(self.SCORE_SIZE)
        self.font_score.bold    = True
        self.bg                 = Surface((self.TILE_WIDTH * 2 + self.BOX_SPACE, self.TILE_HEIGHT))
        self.bg2                = Surface((self.TILE_WIDTH, self.TILE_HEIGHT))
        self.position           = (0, 0)
        self.bg2_position       = (95, 80)

        self._num_move          = 0

        self.redraw()
    
    def reset(self):
        self._current_score     = 0
        self.draw_box_idx(0)
        self._num_move          = 0
        self.draw_box(self.bg2, self._num_move, self.titles[2], 0, 0)

    def add_to_score(self, value: int):
        """
        Add value to current score
        Parameters
        ----------
            value: int
        """
        self._current_score    += value
        self.draw_box_idx(0)
        if self._best_score < self._current_score:
            self._best_score    = self._current_score
            self.draw_box_idx(1)

    def inc_num_move(self, value: int = 1):
        self._num_move += value
        self.draw_box(self.bg2, self._num_move, self.titles[2], 0, 0)
        
    def redraw(self):
        self.bg.fill(self.BACKGROUND_COLOR)
        self.bg2.fill(self.BACKGROUND_COLOR)
        self.draw_box_idx(0)
        self.draw_box_idx(1)
        self.draw_box(self.bg2, self._num_move, self.titles[2], 0, 0)

    def draw_box_idx(self, idx: int):
        if idx == 0:
            self.draw_box(self.bg, self._current_score, self.titles[0], 0, 0)
        elif idx == 1:
            self.draw_box(self.bg, self._best_score, self.titles[1], self.TILE_WIDTH + self.BOX_SPACE, 0)

    def draw_box(self, bg, score: int, title: str, x: int, y: int):
        pygame_draw.rect(bg, self.BOX_COLOR, (x, y, self.TILE_WIDTH, self.TILE_HEIGHT))

        y                      += self.TOP_MARGIN
        text                    = self.font_title.render(title, True, self.TITLE_COLOR)
        w, h                    = text.get_size()
        x_new                   = x + (self.TILE_WIDTH - w) / 2
        bg.blit(text, (x_new, y, w, h))

        y                      += self.font_title.get_linesize() + self.INSIDE_SPACE
        text                    = self.font_score.render(str(score), True, self.SCORE_COLOR)
        w, h                    = text.get_size()
        x_new                   = x + (self.TILE_WIDTH - w) / 2
        bg.blit(text, (x_new, y, w, h))

    def draw(self, screen):
        w, h                    = self.bg.get_size()
        x, y                    = self.position
        screen.blit(self.bg, (x, y, w, h))

        w, h                    = self.bg2.get_size()
        x, y                    = self.bg2_position
        x                      += self.position[0]
        y                      += self.position[1]
        screen.blit(self.bg2, (x, y, w, h))

    @property
    def current_score(self) -> int:
        return self._current_score


    