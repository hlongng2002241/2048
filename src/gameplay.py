import pygame
from pygame.event import Event
from . utility import SharedFont
from game.grid import Grid
from game.score import Score
from game.state import State
from algorithm.minimax_alpha_beta import MinimaxAlphaBeta


class GamePlay:
    # Game Mode
    MODE_AI                     = 1
    MODE_HUMAN                  = 2
    
    def __init__(self) -> None:
        self.current_time       = 0
        self.PLAY_MODE          = self.MODE_HUMAN

        # Limit if move per second
        self.MOVES_PER_SECOND   = 10

        self.score              = Score()
        self.score.position     = (235, 50)
        
        self.grid               = Grid(self.score)
        self.grid.position      = (30, 200)

        font                    = SharedFont().get_font(72)
        font.bold               = True
        self.game_name          = font.render("2048", True, (118, 110, 102))
        self.game_name_pos      = (30, 21)

        # Declaration of algorithm, default: Minimax
        self.algorithm          = MinimaxAlphaBeta(4)  # change this None

        self.state              = State("log.txt")
        self.is_loaded          = False
        
        if self.is_loaded is True:
            self.state.load_file()
            self.state.load_next(self.grid.board)
        else:
            self.state.save_file()
            self.state.save_next(self.grid.board)

    def new_game(self):
        self.grid.restart()
        self.score.reset_current_score()
        self.current_time       = 0

    def set_play_mode(self, mode):
        self.PLAY_MODE          = mode
        self.current_time       = 0

    def set_algorithm(self, algo):
        self.algorithm          = algo
        self.current_time       = 0

    def set_moves_per_second(self, moves):
        self.MOVES_PER_SECOND   = moves
        self.current_time       = 0

    def process_input(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if self.PLAY_MODE == self.MODE_HUMAN and self.grid.is_terminal("max") is False:
                if event.key == pygame.K_LEFT:
                    if self.grid.can_move_left():
                        self.grid.move_left(True)
                        self.grid.random_new_tile()
                        self.grid.redraw()

                elif event.key == pygame.K_RIGHT:
                    if self.grid.can_move_right():
                        self.grid.move_right(True)
                        self.grid.random_new_tile()
                        self.grid.redraw()

                elif event.key == pygame.K_UP:
                    if self.grid.can_move_up():
                        self.grid.move_up(True)
                        self.grid.random_new_tile()
                        self.grid.redraw()

                elif event.key == pygame.K_DOWN:
                    if self.grid.can_move_down():
                        self.grid.move_down(True)
                        self.grid.random_new_tile()
                        self.grid.redraw()

    def update(self, dt):
        if self.grid.is_terminal("max") is False:
            if self.PLAY_MODE == self.MODE_AI:
                self.current_time      += dt
                TIME_PER_MOVE           = 1.0 / self.MOVES_PER_SECOND
                
                if self.current_time >= TIME_PER_MOVE:
                    self.current_time -= TIME_PER_MOVE

                    if self.is_loaded is False:
                        # move_to_make = self.algorithm.best_move(self.grid)
                        # self.grid.move(move_to_make)
                        self.algorithm.best_move(self.grid)
                        self.grid.random_new_tile()
                        self.grid.redraw()
                        self.state.save_next(self.grid.board)
                    else:
                        self.state.load_next(self.grid.board)
                        self.grid.redraw()

    def draw(self, screen: pygame.Surface):
        x, y                    = self.game_name_pos
        w, h                    = self.game_name.get_size()
        screen.blit(self.game_name, (x, y, w, h))

        self.score.draw(screen)
        self.grid.draw(screen)
