from pygame import Surface
from pygame.event import Event
import pygame
from ui.button import Button
from ui.form import Form
from ui.label import Label
from . gameplay import GamePlay
from algorithm.expectimax import Expectimax
from algorithm.minimax import Minimax
from algorithm.minimax_alpha_beta import MinimaxAlphaBeta
from algorithm.mixed_expectimax import MixedExpectimax
from . utility import DevelopmentMode


class Menu:
    def __init__(self, gameplay:GamePlay) -> None:
        self.__gameplay                 = gameplay
        self.position                   = (0, 0)
        self.__menu                     = Form(self)
        self.__depth                    = 4

        font_size                       = 24
        form_mode                       = Form(self.__menu)
        form_mode.position              = (0, 27)
        Label("Game Mode:", font_size, 10, 0, form_mode)
        Button("AI", font_size, 0, 34, 175, 40, form_mode).callback                     = lambda: self.__gameplay.set_play_mode(self.__gameplay.MODE_AI)
        Button("Human", font_size, 180, 34, 175, 40, form_mode).set_state(Button.TOGGLE).callback = lambda: self.__gameplay.set_play_mode(self.__gameplay.MODE_HUMAN)

        form_algo                       = Form(self.__menu)
        form_algo.position              = (0, 118)
        Label("Algorithm:", font_size, 10, -4, form_algo)
        Button("Minimax", font_size, 0, 32, 175, 70, form_algo).callback                = lambda: self.__gameplay.set_algorithm(Minimax(self.__depth))
        Button("Minimax AB", font_size, 180, 32, 175, 70, form_algo).set_state(Button.TOGGLE).callback = lambda: self.__gameplay.set_algorithm(MinimaxAlphaBeta(self.__depth))
        Button("Expectimax", font_size, 0, 107, 175, 70, form_algo).callback            = lambda: self.__gameplay.set_algorithm(Expectimax(self.__depth))
        Button("Mixed", font_size, 180, 107, 175, 70, form_algo).callback               = lambda: self.__gameplay.set_algorithm(MixedExpectimax(self.__depth))


        form_move                       = Form(self.__menu)
        form_move.position              = (0, 312)
        Label("Moves per second:", font_size, 10, -5, form_move)
        Button("5", font_size, 0, 31, 85, 40, form_move).callback                       = lambda: self.__gameplay.set_moves_per_second(5)
        Button("10", font_size, 90, 31, 85, 40, form_move).set_state(Button.TOGGLE).callback = lambda: self.__gameplay.set_moves_per_second(10)
        Button("20", font_size, 180, 31, 85, 40, form_move).callback                    = lambda: self.__gameplay.set_moves_per_second(20)
        Button("100", font_size, 270, 31, 85, 40, form_move).callback                   = lambda: self.__gameplay.set_moves_per_second(100)

        form_depth                      = Form(self.__menu)
        form_depth.position             = (0, 403)
        Label("Max depth:", font_size, 10, -5, form_depth)
        Button("1", font_size, 0, 32, 115, 40, form_depth).callback                     = lambda: self.__set_depth(1)
        Button("2", font_size, 120, 32, 115, 40, form_depth).callback                   = lambda: self.__set_depth(2)
        Button("3", font_size, 240, 32, 115, 40, form_depth).callback                   = lambda: self.__set_depth(3)
        Button("4", font_size, 0, 77, 115, 40, form_depth).set_state(Button.TOGGLE).callback = lambda: self.__set_depth(4)
        Button("5", font_size, 120, 77, 115, 40, form_depth).callback                   = lambda: self.__set_depth(5)
        Button("6", font_size, 240, 77, 115, 40, form_depth).callback                   = lambda: self.__set_depth(6)

        self.__new_game                 = Button("New Game", 22, -400, 80, 150, 50, self)
        self.__new_game.callback        = lambda: self.__button_new_game_callback()

    def __button_new_game_callback(self):
        self.__gameplay.new_game()
        self.__new_game.set_state(Button.NORMAL)

    def __set_depth(self, depth):
        self.__depth                    = depth
        self.__gameplay.current_time    = 0
        self.__gameplay.algorithm.set_max_depth(depth)

    def process_input(self, event: Event):
        self.__menu.process_input(event)
        self.__new_game.process_input(event)

        if DevelopmentMode().on():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.__gameplay.switch_replay_mode()

    def draw(self, screen: Surface):
        self.__menu.draw(screen)
        self.__new_game.draw(screen)
