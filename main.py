import pygame
import pygame.time as pygame_time
import pygame.display as pygame_display
from grid import Grid


class Application:
    """
    this is the main application
    """

    # Game Mode
    MODE_AI             = 1
    MODE_HUMAN          = 2
    PLAY_MODE           = MODE_HUMAN

    # Limit if move per second
    MOVE_PER_SECOND     = 200
    
    def __init__(self):
        pygame.init()
        self.window     = pygame_display.set_mode((600, 600))

        self.grid       = Grid()

        # Declaration of minimax algorithm 
        self.minimax    = None  # change this None

    def show_fps(self, dt: float):
        """
        Show the FPS in window caption
        
        Parameter
        ---------
            dt: delta time, in miliseconds
        """
        if dt == 0:
            return
        fps = 1000 / dt
        pygame_display.set_caption("fps = " + str(fps))

    def run(self):
        """
        Execution function
        """
        running             = True
        start_time          = pygame_time.get_ticks()
        current_time        = 0
        TIME_PER_MOVE       = 1.0 / self.MOVE_PER_SECOND
        
        while running:
            end_time        = pygame_time.get_ticks()
            dt              = end_time - start_time
            start_time      = end_time
            current_time   += dt / 1000

            self.show_fps(dt)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if self.PLAY_MODE == self.MODE_HUMAN and self.grid.has_no_move() is False:
                        if event.key == pygame.K_LEFT:
                            if self.grid.move_left():
                                self.grid.random_new_cell()
                                self.grid.redraw()
                        elif event.key == pygame.K_RIGHT:
                            if self.grid.move_right():
                                self.grid.random_new_cell()
                                self.grid.redraw()
                        elif event.key == pygame.K_UP:
                            if self.grid.move_up():
                                self.grid.random_new_cell()
                                self.grid.redraw()
                        elif event.key == pygame.K_DOWN:
                            if self.grid.move_down():
                                self.grid.random_new_cell()
                                self.grid.redraw()

            if self.grid.has_no_move() is False:
                if self.PLAY_MODE == self.MODE_AI:
                    if current_time >= TIME_PER_MOVE:
                        current_time -= TIME_PER_MOVE
                        self.minimax.best_move(self.grid)
                        self.grid.random_new_cell()
                        self.grid.redraw()

            self.window.fill((255, 255, 255))
            self.grid.draw(self.window)
            pygame.display.flip()

        pygame.quit()


app = Application()
app.run()
