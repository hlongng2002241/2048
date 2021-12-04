from pygame import Surface
import pygame.draw as pygame_draw
from src.utility import SharedFont
import random
from . score import Score
from typing import Tuple, List


class GridSettings:
    BG_COLOR                = {
        0                   : (205, 193, 180),
        2                   : (238, 228, 218),
        4                   : (237, 224, 200),
        8                   : (242, 177, 121),
        16                  : (245, 149, 99),
        32                  : (246, 124, 96),
        64                  : (246, 94, 59),
        128                 : (237, 207, 114),
        256                 : (237, 204, 97),
        512                 : (237, 200, 80),
        1024                : (237, 197, 63),
        2048                : (237, 194, 46),
        4096                : (60, 58, 50),
    }

    COLOR                   = {
        2                   : (119, 110, 101),
        4                   : (119, 110, 101),
        8                   : (249, 246, 242),
        16                  : (249, 246, 242),
        32                  : (249, 246, 242),
        64                  : (249, 246, 242),
        128                 : (249, 246, 242),
        256                 : (249, 246, 242),
        512                 : (249, 246, 242),
        1024                : (249, 246, 242),
        2048                : (249, 246, 242),
        4096                : (249, 246, 242),
    }

    BORDER_COLOR            = (187, 173, 160)

    BORDER_SIZE             = 10
    BORDER_RADIUS           = 0
    TILE_SIZE               = 80


class Grid:
    ROW                     = 4
    COLUMN                  = 4
    RANDOM_4_RATE           = 0.05
    RAMDOM_RANGE            = 1000

    def __init__(self, score: Score):
        self.score          = score

        self.board          = [[0 for c in range(self.COLUMN)] for r in range(self.ROW)]
        self.settings       = GridSettings()

        size                = (
            self.settings.BORDER_SIZE * (self.ROW + 1)
            + self.settings.TILE_SIZE * self.ROW
        )
        self.bg             = Surface((size, size))
        self.font           = SharedFont().get_font(34)
        self.font.bold      = True
        self.position       = (0, 0)

        self.random_new_tile()
        self.random_new_tile()
        self.redraw()

    def has_no_move(self, board: list = None) -> bool:
        """
        I recommend to use is_terminal instead as this function will be removed soon
        
        Parameter
        --------
            board: list, default = None
                if board is None grid's board is used
        
        Return
        ------
            bool: 
        """
        if board is None:
            board = self.board

        # check if there is any empty tile
        for row in board:
            for x in row:
                if x == 0:
                    return False

        # check if there is any adjacent tiles which have the same value
        for r in range(Grid.ROW):
            for c in range(Grid.COLUMN):
                if 0 <= r + 1 < Grid.ROW and board[r][c] == board[r + 1][c]:
                    return False
                if 0 <= c + 1 < Grid.COLUMN and board[r][c] == board[r][c + 1]:
                    return False
        
        return True

    def random_new_tile(self):
        """
        Random new tile in self.board
        """
        # check empty tile
        is_full = True
        for row in self.board:
            for x in row:
                if x == 0:
                    is_full = False
                    break
        if is_full:
            return

        # random tile's value
        tile_value = random.randint(1, self.RAMDOM_RANGE)
        if tile_value > self.RAMDOM_RANGE * (1 - self.RANDOM_4_RATE):
            tile_value = 4
        else:
            tile_value = 2

        # random tile's position
        while True:
            r, c = random.randint(0, self.ROW - 1), random.randint(0, self.COLUMN - 1)
            if self.board[r][c] == 0:
                self.board[r][c] = tile_value
                return

    def draw_tile(self, r, c, tile_value):
        """
        Draw single tile
        """
        # draw background
        size                = self.settings.BORDER_SIZE + self.settings.TILE_SIZE
        x                   = self.settings.BORDER_SIZE + size * c
        y                   = self.settings.BORDER_SIZE + size * r
        bg_color            = self.settings.BG_COLOR[tile_value]
        pygame_draw.rect(
            self.bg,
            bg_color,
            (x, y, self.settings.TILE_SIZE, self.settings.TILE_SIZE),
            border_radius=self.settings.BORDER_RADIUS,
        )

        if tile_value == 0:
            return

        # draw foreground: tile's value
        color               = self.settings.COLOR[tile_value]
        text_surface        = self.font.render(str(tile_value), True, color)
        w, h                = text_surface.get_width(), text_surface.get_height()
        cell_size           = self.settings.TILE_SIZE
        x                  += (cell_size - w) / 2
        y                  += (cell_size - h) / 2
        self.bg.blit(text_surface, (x, y, w, h))

    def redraw(self):
        """
        Redraw entire board
        """
        self.bg.fill(self.settings.BORDER_COLOR)

        for r in range(self.ROW):
            for c in range(self.COLUMN):
                self.draw_tile(r, c, self.board[r][c])

    def draw(self, screen: Surface):
        """
        Draw
        """
        w, h                = self.bg.get_size()
        x, y                = self.position

        screen.blit(self.bg, (x, y, w, h))

    def restart(self):
        self.board          = [[0 for c in range(self.COLUMN)] for r in range(self.ROW)]
        self.random_new_tile()
        self.random_new_tile()
        self.redraw()

    @staticmethod
    def copy(src: list, des: list):
        """
        This function is used to copy the board's values

        Parameters
        ----------
            src: list
                source
            
            des: list
                destination
        """
        des.clear()
        ROW, COLUMN = Grid.ROW, Grid.COLUMN
        for r in range(ROW):
            des.append([])
            for c in range(COLUMN):
                des[r].append(src[r][c])

    def can_move_up(self) -> bool:
        """
        Returns
        -------
            True if can move, else False
        """
        # loop for all columns
        # start at the bottom and move upwards until find a non-empty element
        # then, check that there are 2 similar adjacent tiles or there is an empty square
        ROW, COLUMN = self.ROW, self.COLUMN

        for j in range(COLUMN):
            k = -1
            for i in range(ROW - 1, -1, -1):
                if self.board[i][j] != 0:
                    k = i
                    break

            if k != -1:
                for i in range(k, 0, -1):
                    if (
                        self.board[i - 1][j] == 0
                        or self.board[i][j] == self.board[i - 1][j]
                    ):
                        return True
        return False

    def can_move_down(self) -> bool:
        """
        Returns
        -------
            True if can move, else False
        """
        ROW = self.ROW
        COLUMN = self.COLUMN

        for j in range(COLUMN):
            k = -1
            for i in range(ROW):
                if self.board[i][j] != 0:
                    k = i
                    break

            if k != -1:
                for i in range(k, ROW - 1):
                    if (
                        self.board[i + 1][j] == 0
                        or self.board[i + 1][j] == self.board[i][j]
                    ):
                        return True
        return False

    def can_move_left(self) -> bool:
        """
        Returns
        -------
            True if can move, else False
        """
        ROW = self.ROW
        COLUMN = self.COLUMN

        for i in range(ROW):
            k = -1
            for j in range(COLUMN - 1, -1, -1):
                if self.board[i][j] != 0:
                    k = j
                    break
            
            if k != -1:
                for j in range(k, 0, -1):
                    if (
                        self.board[i][j - 1] == 0
                        or self.board[i][j - 1] == self.board[i][j]
                    ):
                        return True
        return False

    def can_move_right(self) -> bool:
        """
        Returns
        -------
            True if can move, else False
        """
        ROW = self.ROW
        COLUMN = self.COLUMN

        for i in range(ROW):
            k = -1
            for j in range(COLUMN):
                if self.board[i][j] != 0:
                    k = j
                    break
            if k != -1:
                for j in range(k, COLUMN - 1):
                    if (
                        self.board[i][j + 1] == 0
                        or self.board[i][j + 1] == self.board[i][j]
                    ):
                        return True
        return False

    def get_available_moves_for_max(self) -> List[int]:
        """
        Indices for movements:
            Up = 0, Down = 1, Left = 2, Right = 3

        Returns
        -------
            list: list
                list of indices of movements
        """
        available_moves = []

        if self.can_move_up():
            available_moves.append(0)
        if self.can_move_down():
            available_moves.append(1)
        if self.can_move_left():
            available_moves.append(2)
        if self.can_move_right():
            available_moves.append(3)

        return available_moves

    def get_available_moves_for_min(self) -> List[Tuple[int, int, int]]:
        """
        In some case, min can be understood as expect
        """
        empty_squares = []
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                if self.board[i][j] == 0:
                    if random.random() > 0.9:
                        empty_squares.append((i, j, 4))
                    else:
                        empty_squares.append((i, j, 2))
        return empty_squares

    def get_num_empty_tiles(self) -> int:
        return len(self.get_available_moves_for_min())

    def place_tile(self, row: int, column: int, tile: int) -> None:
        """
        Set value for tile at row 'row' and column 'column'
        """
        self.board[row][column] = tile

    def get_children(self, who: str) -> list:
        """
        Get next grid states

        Parameters
        ----------
            who: str
                who can be "max", "min" or "expect"

        Returns
        -------
            list of next available moves (or grid states)
        """
        if who == "max":
            return self.get_available_moves_for_max()
        elif who == "min" or who == "expect":
            return self.get_available_moves_for_min()

    def move_up(self, calculate_score=False) -> None:
        """
        Move entire tiles in self.board towards up border

        Parameters
        ----------
            calculate_score: bool, default = False
                decide if this movement is scored or not
        """
        ROW, COLUMN = self.ROW, self.COLUMN
        # Loop over all columns
        for j in range(COLUMN):
            # w: the location of the write operation
            # k: the tile value of the last non-empty cell
            w = k = 0
            for i in range(ROW):
                # skip empty cells
                if self.board[i][j] == 0:
                    continue
                # store the value of the next non-empty cell in k
                if k == 0:
                    k = self.board[i][j]
                # merge 2 same tiles and write the result at location w
                # increase w and reset k = 0
                elif self.board[i][j] == k:
                    self.board[w][j] = 2 * k
                    if calculate_score is True:
                        self.score.add(2 * k)
                    w += 1
                    k = 0
                # if 2 tiles don't match, write the first tile at location w
                # increase w and store the second one in k
                else:
                    self.board[w][j] = k
                    w += 1
                    k = self.board[i][j]
            # after the loop ends, if k still != 0, write this value at location w and increase w
            if k != 0:
                self.board[w][j] = k
                w += 1
            # empty all cells from w downwards
            for i in range(w, ROW):
                self.board[i][j] = 0

    def move_down(self, calculate_score=False) -> None:
        """
        Move entire tiles in self.board towards down border

        Parameters
        ----------
            calculate_score: bool, default = False
                decide if this movement is scored or not
        """
        ROW, COLUMN = self.ROW, self.COLUMN

        for j in range(COLUMN):
            w, k = 3, 0
            for i in range(ROW - 1, -1, -1):
                if self.board[i][j] == 0:
                    continue
                if k == 0:
                    k = self.board[i][j]
                elif k == self.board[i][j]:
                    self.board[w][j] = 2 * k
                    if calculate_score is True:
                        self.score.add(2 * k)
                    w -= 1
                    k = 0
                else:
                    self.board[w][j] = k
                    w -= 1
                    k = self.board[i][j]
            if k != 0:
                self.board[w][j] = k
                w -= 1
            for i in range(w, -1, -1):
                self.board[i][j] = 0

    def move_left(self, calculate_score=False) -> None:
        """
        Move entire tiles in self.board towards left border

        Parameters
        ----------
            calculate_score: bool, default = False
                decide if this movement is scored or not
        """
        ROW, COLUMN = self.ROW, self.COLUMN

        for i in range(ROW):
            w = k = 0
            for j in range(COLUMN):
                if self.board[i][j] == 0:
                    continue
                if k == 0:
                    k = self.board[i][j]
                elif k == self.board[i][j]:
                    self.board[i][w] = 2 * k
                    if calculate_score is True:
                        self.score.add(2 * k)
                    w += 1
                    k = 0
                else:
                    self.board[i][w] = k
                    w += 1
                    k = self.board[i][j]
            if k != 0:
                self.board[i][w] = k
                w += 1
            for j in range(w, COLUMN):
                self.board[i][j] = 0

    def move_right(self, calculate_score=False) -> None:
        """
        Move entire tiles in self.board towards right border

        Parameters
        ----------
            calculate_score: bool, default = False
                decide if this movement is scored or not
        """
        ROW, COLUMN = self.ROW, self.COLUMN

        for i in range(ROW):
            w, k = 3, 0
            for j in range(COLUMN - 1, -1, -1):
                if self.board[i][j] == 0:
                    continue
                if k == 0:
                    k = self.board[i][j]
                elif k == self.board[i][j]:
                    self.board[i][w] = 2 * k
                    if calculate_score is True:
                        self.score.add(2 * k)
                    w -= 1
                    k = 0
                else:
                    self.board[i][w] = k
                    w -= 1
                    k = self.board[i][j]
            if k != 0:
                self.board[i][w] = k
                w -= 1
            for j in range(w + 1):
                self.board[i][j] = 0

    def move(self, direction: int, calculate_score=False) -> None:
        """
        Indices for directions:
            Up = 0, Down = 1, Left = 2, Right = 3

        Parameters
        ----------
        direction: int

        calculate_score: bool
        """
        if direction == 0:
            self.move_up(calculate_score)
        elif direction == 1:
            self.move_down(calculate_score)
        elif direction == 2:
            self.move_left(calculate_score)
        else:
            self.move_right(calculate_score)

    def is_terminal(self, who: str) -> bool:
        """
        Check if the current grid state is end for "who" or not
        
        Parameters
        ----------
            who: str
                who can be "max", "min" or "expect"

        Returns
        -------
            is_terminal: bool
        """
        if who == "max":
            if self.can_move_up():
                return False
            if self.can_move_down():
                return False
            if self.can_move_left():
                return False
            if self.can_move_right():
                return False
            return True
        elif who == "min" or who == "expect":
            for i in range(4):
                for j in range(4):
                    if self.board[i][j] == 0:
                        return False
            return True
