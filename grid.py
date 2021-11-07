from pygame import Surface
import pygame.font as pygame_font
import pygame.draw as pygame_draw
import random

class GridSettings:
    BG_COLOR            = {
        0               : (205, 193, 180),
        2               : (238, 228, 218),
        4               : (237, 224, 200),
        8               : (242, 177, 121),
        16              : (245, 149,  99),
        32              : (246, 124,  96),
        64              : (246,  94,  59),
        128             : (237, 207, 114),
        256             : (237, 204,  97),
        512             : (237, 200,  80),
        1024            : (237, 197,  63),
        2048            : (237, 194,  46),
        4096            : ( 60,  58,  50),
    }

    COLOR               = {
        2               : (119, 110, 101),
        4               : (119, 110, 101),
        8               : (249, 246, 242),
        16              : (249, 246, 242),
        32              : (249, 246, 242),
        64              : (249, 246, 242),
        128             : (249, 246, 242),
        256             : (249, 246, 242),
        512             : (249, 246, 242),
        1024            : (249, 246, 242),
        2048            : (249, 246, 242),
        4096            : (249, 246, 242),
    }

    BORDER_COLOR        = (187, 173, 160)

    BORDER_SIZE         = 10
    BORDER_RADIUS       = 0
    TILE_SIZE           = 80
    

class Grid:
    ROW                 = 4
    COLUMN              = 4
    RANDOM_4_RATE       = 0.05
    RAMDOM_RANGE        = 1000
    
    def __init__(self):
        self.board      = [[0 for c in range(self.COLUMN)] for r in range(self.ROW)]
        self.settings   = GridSettings()
        
        size            = self.settings.BORDER_SIZE * (self.ROW + 1) + self.settings.TILE_SIZE * self.ROW
        self.bg         = Surface((size, size))
        self.font       = pygame_font.Font("fonts/JetBrains.ttf", 34)
        self.position   = (50, 50)

        self.random_new_cell()
        self.random_new_cell()
        self.redraw()

    def has_no_move(self) -> bool:
        # check if there is any empty tile
        for row in self.board:
            for x in row:
                if x == 0:
                    return False

        # check if there is any adjacent tiles which have the same value
        for r in range(self.ROW):
            for c in range(self.COLUMN):
                if 0 <= r + 1 < self.ROW and self.board[r][c] == self.board[r + 1][c]:
                    return False
                if 0 <= c + 1 < self.COLUMN and self.board[r][c] == self.board[r][c + 1]:
                    return False
        
        return True
        
    def random_new_cell(self):
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
        size            = self.settings.BORDER_SIZE + self.settings.TILE_SIZE
        x               = self.settings.BORDER_SIZE + size * c
        y               = self.settings.BORDER_SIZE + size * r
        bg_color        = self.settings.BG_COLOR[tile_value]
        pygame_draw.rect(self.bg, bg_color, (x, y, self.settings.TILE_SIZE, self.settings.TILE_SIZE), border_radius=self.settings.BORDER_RADIUS)

        if tile_value == 0:
            return
        
        # draw foreground: tile's value
        color           = self.settings.COLOR[tile_value]
        text_surface    = self.font.render(str(tile_value), True, color)
        w, h            = text_surface.get_width(), text_surface.get_height()
        cell_size       = self.settings.TILE_SIZE
        x               += (cell_size - w) / 2
        y               += (cell_size - h) / 2
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
        w, h = self.bg.get_size()
        x, y = self.position

        screen.blit(self.bg, (x, y, w, h))

    @staticmethod
    def copy(src: list, des: list):
        """
        This function is used to copy the board's values
        """
        des.clear()
        ROW, COLUMN = Grid.ROW, Grid.COLUMN
        for r in range(ROW):
            des.append([])
            for c in range(COLUMN):
                des[r].append(src[r][c])

    def move_left(self) -> bool:
        """
        return True if can merge, else False
        """
        is_merged   = False
        ROW         = self.ROW
        COLUMN      = self.COLUMN

        for r in range(ROW):
            used    = [0 for c in range(COLUMN)]

            for c in range(1, COLUMN):
                if self.board[r][c] == 0:
                    continue
                
                k = c - 1
                while k >= 0 and self.board[r][k] == 0:
                    k -= 1
                
                if k == -1:
                    self.board[r][0]            = self.board[r][c]
                    self.board[r][c]            = 0
                    is_merged                   = True
                    continue
                    
                if self.board[r][k] == self.board[r][c] and used[k] == 0:
                    self.board[r][k]            *= 2
                    self.board[r][c]            = 0
                    used[k]                     = 1
                    is_merged                   = True
                else:
                    if k + 1 != c:
                        self.board[r][k + 1]    = self.board[r][c]
                        self.board[r][c]        = 0
                        is_merged               = True

        return is_merged

    def move_right(self) -> bool:
        is_merged   = False
        ROW         = self.ROW
        COLUMN      = self.COLUMN

        for r in range(ROW):
            used    = [0 for c in range(COLUMN)]

            for c in range(COLUMN - 2, -1, -1):
                if self.board[r][c] == 0:
                    continue
                
                k = c + 1
                while k < COLUMN and self.board[r][k] == 0:
                    k += 1
                
                if k == COLUMN:
                    self.board[r][k - 1]        = self.board[r][c]
                    self.board[r][c]            = 0
                    is_merged                   = True
                    continue
                    
                if self.board[r][k] == self.board[r][c] and used[k] == 0:
                    self.board[r][k]            *= 2
                    self.board[r][c]            = 0
                    used[k]                     = 1
                    is_merged                   = True
                else:
                    if k - 1 != c:
                        self.board[r][k - 1]    = self.board[r][c]
                        self.board[r][c]        = 0
                        is_merged               = True

        return is_merged

    def move_up(self) -> bool:
        is_merged   = False
        ROW         = self.ROW
        COLUMN      = self.COLUMN

        for c in range(COLUMN):
            used    = [0 for r in range(ROW)]

            for r in range(1, ROW):
                if self.board[r][c] == 0:
                    continue
                
                k = r - 1
                while k >= 0 and self.board[k][c] == 0:
                    k -= 1
                
                if k == -1:
                    self.board[0][c]            = self.board[r][c]
                    self.board[r][c]            = 0
                    is_merged                   = True
                    continue
                    
                if self.board[k][c] == self.board[r][c] and used[k] == 0:
                    self.board[k][c]            *= 2
                    self.board[r][c]            = 0
                    used[k]                     = 1
                    is_merged                   = True
                else:
                    if k + 1 != r:
                        self.board[k + 1][c]    = self.board[r][c]
                        self.board[r][c]        = 0
                        is_merged               = True

        return is_merged

    def move_down(self) -> bool:
        is_merged   = False
        ROW         = self.ROW
        COLUMN      = self.COLUMN

        for c in range(COLUMN):
            used    = [0 for r in range(ROW)]
            
            for r in range(ROW - 2, -1, -1):
                if self.board[r][c] == 0:
                    continue
                
                k = r + 1
                while k < ROW and self.board[k][c] == 0:
                    k += 1
                
                if k == ROW:
                    self.board[k - 1][c]        = self.board[r][c]
                    self.board[r][c]            = 0
                    is_merged                   = True
                    continue
                    
                if self.board[k][c] == self.board[r][c] and used[k] == 0:
                    self.board[k][c]            *= 2
                    self.board[r][c]            = 0
                    used[k]                     = 1
                    is_merged                   = True
                else:
                    if k - 1 != r:
                        self.board[k - 1][c]    = self.board[r][c]
                        self.board[r][c]        = 0
                        is_merged               = True

        return is_merged
