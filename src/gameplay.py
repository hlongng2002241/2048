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
        self.score.position     = (215, 50)
        
        self.grid               = Grid(self.score)
        self.grid.position      = (30, 200)

        font                    = SharedFont().get_font(74)
        font.bold               = True
        self.game_name          = font.render("2048", True, (12, 55, 66))
        self.game_name_pos      = (30, 21)

        # Declaration of algorithm, default: Minimax
        self.algorithm          = MinimaxAlphaBeta(4)  # change this None

        self.state              = State("log.txt")
        self.is_replayed        = False
        
        if self.is_replayed is True:
            self.state.load_file()
            self.state.load_next(self.grid.board)
        else:
            self.state.save_file()
            self.state.save_next(self.grid.board)

        # =================================================
        # Statistics here
        self.is_statistics      = False
        self.n_statistics       = 100
        self.idx_statistics     = 0
        self.__file_statistics  = open("stat.out", "w")
        # =================================================


    def new_game(self):
        self.grid.restart()
        self.score.reset()
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

                    if self.is_replayed is False:
                        self.algorithm.best_move(self.grid)
                        self.grid.random_new_tile()
                        self.grid.redraw()
                        self.state.save_next(self.grid.board)
                    else:
                        self.state.load_next(self.grid.board)
                        self.grid.redraw()
        else:
            self.__do_statistics()
            
    def __do_statistics(self):
        if self.is_statistics is False:
            return
        
        if self.idx_statistics + 1 < self.n_statistics:
            self.idx_statistics += 1
            self.__prompt_result_for_statistic()
            self.new_game()
            self.state.close()
            if self.is_replayed:
                self.state.load_file()
            else:
                self.state.save_file()
        elif self.idx_statistics + 1 == self.n_statistics:
            self.idx_statistics += 1
            self.__prompt_result_for_statistic()
            self.idx_statistics += 1 
            self.__file_statistics.close()

    def __prompt_result_for_statistic(self):
        max_tile = 0
        for row in self.grid.board:
            for x in row:
                max_tile = max(max_tile, x)

        n_movements = self.state.idx + 1
        score = self.score.current_score

        print(self.idx_statistics, "/", self.n_statistics)
        print("max_tile:", max_tile)
        print("movements:", n_movements)
        print("score:", score)
        print()

        f = self.__file_statistics
        f.write(f"{self.idx_statistics} / {self.n_statistics}\n")
        f.write(f"max_tile: {max_tile}\n")
        f.write(f"movements: {n_movements}\n")
        f.write(f"score: {score}\n\n")

    def draw(self, screen: pygame.Surface):
        x, y                    = self.game_name_pos
        w, h                    = self.game_name.get_size()
        screen.blit(self.game_name, (x, y, w, h))

        self.score.draw(screen)
        self.grid.draw(screen)
