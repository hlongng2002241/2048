from pygame import Surface
from ui.button import Button
from ui.form import Form
from ui.label import Label
from . gameplay import GamePlay
# from algorithm.expectmax import Expectmax
from algorithm.minimax import Minimax
# from algorithm.minimax_alpha_beta import MinimaxAlphaBeta
# from algorithm.mixed_expectmax import MixedExpectmaxMinimax


class Menu:
    def __init__(self, gameplay:GamePlay) -> None:
        self.gameplay               = gameplay
        self.position               = (0, 0)
        self.menu                   = Form(self)
        self.depth                  = 4

        font_size                   = 24
        form_mode                   = Form(self.menu)
        form_mode.position          = (0, 27)
        Label("Game Mode:", font_size, 10, 0, form_mode)
        Button("AI", font_size, 0, 34, 175, 40, form_mode).callback                 = lambda: self.gameplay.set_play_mode(self.gameplay.MODE_AI)
        Button("Human", font_size, 180, 34, 175, 40, form_mode).set_state(Button.TOGGLE).callback = lambda: self.gameplay.set_play_mode(self.gameplay.MODE_HUMAN)

        form_algo                   = Form(self.menu)
        form_algo.position          = (0, 118)
        Label("Algorithm:", font_size, 10, -4, form_algo)
        Button("Minimax", font_size, 0, 32, 175, 70, form_algo).callback            = lambda: self.gameplay.set_algorithm(Minimax(self.depth))
        Button("Minimax AB", font_size, 180, 32, 175, 70, form_algo).set_state(Button.TOGGLE).callback = lambda: self.gameplay.set_algorithm(MinimaxAlphaBeta(self.depth))
        Button("Expectmax", font_size, 0, 107, 175, 70, form_algo).callback         = lambda: self.gameplay.set_algorithm(Expectmax(self.depth))
        Button("MixExpectMax", font_size, 180, 107, 175, 70, form_algo).callback    = lambda: self.gameplay.set_algorithm(MixedExpectmaxMinimax(self.depth))


        form_move                   = Form(self.menu)
        form_move.position          = (0, 312)
        Label("Moves per second:", font_size, 10, -5, form_move)
        Button("5", font_size, 0, 31, 85, 40, form_move).callback                   = lambda: self.gameplay.set_moves_per_second(5)
        Button("10", font_size, 90, 31, 85, 40, form_move).set_state(Button.TOGGLE).callback = lambda: self.gameplay.set_moves_per_second(10)
        Button("20", font_size, 180, 31, 85, 40, form_move).callback                = lambda: self.gameplay.set_moves_per_second(20)
        Button("100", font_size, 270, 31, 85, 40, form_move).callback               = lambda: self.gameplay.set_moves_per_second(100)

        form_depth                  = Form(self.menu)
        form_depth.position         = (0, 403)
        Label("Max depth:", font_size, 10, -5, form_depth)
        Button("1", font_size, 0, 32, 115, 40, form_depth).callback                 = lambda: self._set_depth(1)
        Button("2", font_size, 120, 32, 115, 40, form_depth).callback               = lambda: self._set_depth(2)
        Button("3", font_size, 240, 32, 115, 40, form_depth).callback               = lambda: self._set_depth(3)
        Button("4", font_size, 0, 77, 115, 40, form_depth).set_state(Button.TOGGLE).callback = lambda: self._set_depth(4)
        Button("5", font_size, 120, 77, 115, 40, form_depth).callback               = lambda: self._set_depth(5)
        Button("6", font_size, 240, 77, 115, 40, form_depth).callback               = lambda: self._set_depth(6)

        # form_replay                 = Form(self.menu)
        # form_replay.position        = (-400, 85)
        # Label("Replay:", font_size, 0, 0, form_replay)
        # Button("On", font_size, 85, 0, 50, 40, form_replay).callback            = lambda: self._set_replay_mode(True)
        # Button("Off", font_size, 140, 0, 50, 40, form_replay).set_state(Button.TOGGLE).callback = lambda: self._set_replay_mode(False)
        
        self.new_game               = Button("New Game", 22, -400, 80, 150, 50, self)
        self.new_game.callback      = lambda: self._button_new_game()

    def _set_replay_mode(self, on: bool):
        if self.gameplay.is_replayed == on:
            return
        self.gameplay.is_replayed   = on
        self.gameplay.state.switch()

    def _button_new_game(self):
        self.gameplay.new_game()
        self.new_game.set_state(Button.NORMAL)

    def _set_depth(self, depth):
        self.depth                  = depth
        self.gameplay.current_time  = 0
        self.gameplay.algorithm.set_max_depth(depth)

    def process_input(self, event):
        self.menu.process_input(event)
        self.new_game.process_input(event)

    def draw(self, screen: Surface):
        self.menu.draw(screen)
        self.new_game.draw(screen)
