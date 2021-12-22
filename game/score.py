from pygame import Surface
import pygame.draw as pygame_draw
from src.utility import SharedFont


class Score:
    BACKGROUND_COLOR            = (250, 248, 240)
    BOX_COLOR                   = (164, 218, 246)
    SCORE_COLOR                 = (255, 255, 255)
    TITLE_COLOR                 = (12, 55, 66)

    BORDER_RADIUS               = 5

    TITLE_SIZE                  = 16
    SCORE_SIZE                  = 24

    TILE_WIDTH                  = 90
    TILE_HEIGHT                 = 50
    BOX_SPACE                   = 5

    TOP_MARGIN                  = 0
    INSIDE_SPACE                = -5


    def __init__(self) -> None:
        self.__current_score    = 0
        self.__best_score       = 0
        self.__titles           = ['SCORE', 'BEST', 'MOVES']

        self.__font_title       = SharedFont().get_font(self.TITLE_SIZE)
        self.__font_title.bold  = True
        self.__font_score       = SharedFont().get_font(self.SCORE_SIZE)
        self.__font_score.bold  = True
        self.__bg               = Surface((self.TILE_WIDTH * 2 + self.BOX_SPACE, self.TILE_HEIGHT))
        self.__bg2              = Surface((self.TILE_WIDTH, self.TILE_HEIGHT))
        self.position           = (0, 0)
        self.__bg2_position     = (95, 80)

        self.__num_moves        = 0

        self.redraw()

    def reset(self):
        self.__current_score    = 0
        self.__draw_box_idx(0)
        self.__num_moves        = 0
        self.__draw_box(self.__bg2, self.__num_moves, self.__titles[2], 0, 0)

    def inc_num_move(self, value: int = 1):
        self.__num_moves       += value
        self.__draw_box(self.__bg2, self.__num_moves, self.__titles[2], 0, 0)
        
    def redraw(self):
        self.__bg.fill(self.BACKGROUND_COLOR)
        self.__bg2.fill(self.BACKGROUND_COLOR)
        self.__draw_box_idx(0)
        self.__draw_box_idx(1)
        self.__draw_box(self.__bg2, self.__num_moves, self.__titles[2], 0, 0)

    def __draw_box_idx(self, idx: int):
        if idx == 0:
            self.__draw_box(self.__bg, self.__current_score, self.__titles[0], 0, 0)
        elif idx == 1:
            self.__draw_box(self.__bg, self.__best_score, self.__titles[1], self.TILE_WIDTH + self.BOX_SPACE, 0)

    def __draw_box(self, bg, score: int, title: str, x: int, y: int):
        pygame_draw.rect(bg, self.BOX_COLOR, (x, y, self.TILE_WIDTH, self.TILE_HEIGHT), border_radius=self.BORDER_RADIUS)

        y                      += self.TOP_MARGIN
        text                    = self.__font_title.render(title, True, self.TITLE_COLOR)
        w, h                    = text.get_size()
        x_new                   = x + (self.TILE_WIDTH - w) / 2
        bg.blit(text, (x_new, y, w, h))

        y                      += self.__font_title.get_linesize() + self.INSIDE_SPACE
        text                    = self.__font_score.render(str(score), True, self.SCORE_COLOR)
        w, h                    = text.get_size()
        x_new                   = x + (self.TILE_WIDTH - w) / 2
        bg.blit(text, (x_new, y, w, h))

    def draw(self, screen):
        w, h                    = self.__bg.get_size()
        x, y                    = self.position
        screen.blit(self.__bg, (x, y, w, h))

        w, h                    = self.__bg2.get_size()
        x, y                    = self.__bg2_position
        x                      += self.position[0]
        y                      += self.position[1]
        screen.blit(self.__bg2, (x, y, w, h))

    @property
    def current_score(self) -> int:
        return self.__current_score
    
    @current_score.setter
    def current_score(self, score):
        self.__current_score    = score
        self.__draw_box_idx(0)
        if self.__best_score < self.__current_score:
            self.__best_score   = self.__current_score
            self.__draw_box_idx(1)

    @property
    def num_moves(self):
        return self.__num_moves

    @num_moves.setter
    def num_moves(self, value):
        self.__num_moves = value
        self.__draw_box(self.__bg2, self.__num_moves, self.__titles[2], 0, 0)






    




    