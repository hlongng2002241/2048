import pygame
from pygame.event import Event
from . utility import SharedFont, DevelopmentMode
from game.grid import Grid
from game.score import Score
from game.state import State
from algorithm.expectimax import Expectimax
from algorithm.minimax import Minimax
from algorithm.minimax_alpha_beta import MinimaxAlphaBeta
from algorithm.mixed_expectimax import MixedExpectimax

import time
import shutil
import os


class GamePlay:
    # Game Mode
    MODE_AI                     = 1
    MODE_HUMAN                  = 2
    
    def __init__(self) -> None:
        self.current_time       = 0
        self.PLAY_MODE          = self.MODE_HUMAN

        # Limit if move per second
        self.MOVES_PER_SECOND   = 10

        self.__score            = Score()
        self.__score.position   = (215, 50)

        self.__state            = State("log.txt", "save")
        self.__is_replayed      = False
        
        self.__grid             = Grid(self.__score, self.__state)
        self.__grid.position    = (30, 200)

        self.__state.save_next(self.__grid.board, self.__score)

        font                    = SharedFont().get_font(74)
        font.bold               = True
        self.__game_name        = font.render("2048", True, (12, 55, 66))
        self.__game_name_pos    = (30, 21)

        # Declaration of algorithm, default: Minimax
        self.algorithm          = MinimaxAlphaBeta(4)

        # =================================================
        # Statistics here
        self.is_statistics      = False
        self.n_statistics       = 100
        self.idx_statistics     = 0
        self.__file_statistics  = open("stat.out", "w")
        # =================================================
        # first try with d = 5, 20 times

    def new_game(self):
        self.__grid.restart()
        self.__score.reset()

        if DevelopmentMode():
            if self.__is_replayed is False:
                self.__state.open_file("log.txt", "save")
            else:
                self.__load_replay_file(self.algorithm)

        self.current_time       = 0

    def set_play_mode(self, mode):
        self.PLAY_MODE          = mode
        self.current_time       = 0

    def set_algorithm(self, algo):
        self.algorithm          = algo
        self.current_time       = 0

        if DevelopmentMode().on():
            if self.__is_replayed:
                self.__load_replay_file(algo)

    def __load_replay_file(self, algo):
        if self.__state.mode == "load":
            return

        if isinstance(algo, Minimax):
            self.__state.open_file(f"./saved/minimax_d{self.algorithm.max_depth}.out", "load")
        elif isinstance(algo, MinimaxAlphaBeta):
            self.__state.open_file(f"./saved/minimax_ab_d{self.algorithm.max_depth}.out", "load")
        elif isinstance(algo, Expectimax):
            self.__state.open_file(f"./saved/expectimax_d{self.algorithm.max_depth}.out", "load")
        elif isinstance(algo, MixedExpectimax):
            self.__state.open_file(f"./saved/mixed_d{self.algorithm.max_depth}.out", "load")
    
    def switch_replay_mode(self):
        if self.__is_replayed is False:
            self.__is_replayed  = True
            self.__load_replay_file(self.algorithm)
            print("replay mode: ON")
        else:
            self.__is_replayed  = False
            self.__state.open_file("log.txt", "save")
            print("replay mode: OFF")

    def set_moves_per_second(self, moves):
        self.MOVES_PER_SECOND   = moves
        self.current_time       = 0

    def process_input(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if self.PLAY_MODE == self.MODE_HUMAN and self.__grid.is_terminal("max") is False:
                if event.key == pygame.K_LEFT:
                    if self.__grid.can_move_left():
                        self.__grid.move_left(True)
                        self.__grid.random_new_tile()
                        self.__grid.redraw()

                elif event.key == pygame.K_RIGHT:
                    if self.__grid.can_move_right():
                        self.__grid.move_right(True)
                        self.__grid.random_new_tile()
                        self.__grid.redraw()

                elif event.key == pygame.K_UP:
                    if self.__grid.can_move_up():
                        self.__grid.move_up(True)
                        self.__grid.random_new_tile()
                        self.__grid.redraw()

                elif event.key == pygame.K_DOWN:
                    if self.__grid.can_move_down():
                        self.__grid.move_down(True)
                        self.__grid.random_new_tile()
                        self.__grid.redraw()

    def update(self, dt):
        if self.__grid.is_terminal("max") is False:
            if self.PLAY_MODE == self.MODE_AI:
                self.current_time      += dt
                TIME_PER_MOVE           = 1.0 / self.MOVES_PER_SECOND
                
                if self.current_time >= TIME_PER_MOVE:
                    self.current_time  -= TIME_PER_MOVE

                    if self.__is_replayed is False:
                        self.algorithm.best_move(self.__grid)
                        self.__grid.random_new_tile()
                        self.__grid.redraw()
                    else:
                        self.__state.load_next(self.__grid.board, self.__score)
                        self.__grid.redraw()
        else:
            self.__state.close_file("save")
            self.__do_statistics()
    
    def __store_special_log(self):
        src                     = "log.txt"
        des                     = "./saved/log.out"
        shutil.copyfile(src, des)

        if isinstance(self.algorithm, Minimax):
            new_name            = f"./saved/minimax_d{self.algorithm.max_depth}_{int(time.time())}.out"
        elif isinstance(self.algorithm, MinimaxAlphaBeta):
            new_name            = f"./saved/minimax_ab_d{self.algorithm.max_depth}_{int(time.time())}.out"
        elif isinstance(self.algorithm, Expectimax):
            new_name            = f"./saved/expectimax_d{self.algorithm.max_depth}_{int(time.time())}.out"
        elif isinstance(self.algorithm, MixedExpectimax):
            new_name            = f"./saved/mixed_d{self.algorithm.max_depth}_{int(time.time())}.out"

        os.rename(des, new_name)
        
    def __do_statistics(self):
        if self.is_statistics is False:
            return
        
        max_tile = 0
        for row in self.__grid.board:
            for x in row:
                max_tile        = max(max_tile, x)
        
        if max_tile >= 8192:
            self.__store_special_log()
        
        if self.idx_statistics + 1 < self.n_statistics:
            self.idx_statistics += 1
            self.__prompt_result_for_statistic()
            self.new_game()

        elif self.idx_statistics + 1 == self.n_statistics:
            self.idx_statistics += 1
            self.__prompt_result_for_statistic()

            self.idx_statistics += 1 
            self.__file_statistics.close()

    def __prompt_result_for_statistic(self):
        max_tile = 0
        for row in self.__grid.board:
            for x in row:
                max_tile        = max(max_tile, x)

        n_movements             = self.__score.num_moves
        score                   = self.__score.current_score

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
        x, y                    = self.__game_name_pos
        w, h                    = self.__game_name.get_size()
        screen.blit(self.__game_name, (x, y, w, h))

        self.__score.draw(screen)
        self.__grid.draw(screen)
