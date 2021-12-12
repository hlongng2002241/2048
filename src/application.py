import pygame
import pygame.time as pygame_time
import pygame.display as pygame_display
from . gameplay import GamePlay
from . menu import Menu


class Application:
    def __init__(self):
        pygame.init()
        self.screen         = pygame_display.set_mode((815, 600))

        self.gameplay       = GamePlay()

        self.running        = True

        self.menu           = Menu(self.gameplay)
        self.menu.position  = (430, 50)

    def show_fps(self, dt: float):
        """
        Show the FPS in window caption
        
        Parameter
        ---------
            dt: delta time, in miliseconds
        """
        if dt == 0:
            return
        fps = 1.0 / dt
        pygame_display.set_caption("fps = " + str(fps))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            self.gameplay.process_input(event)
            self.menu.process_input(event)
        
    def update(self, dt):
        self.gameplay.update(dt)
    
    def draw(self):
        # self.screen.fill((0, 0, 0))
        self.screen.fill((232, 240, 242))
        
        self.gameplay.draw(self.screen)
        self.menu.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """
        Execution function
        """
        self.running        = True
        start_time          = pygame_time.get_ticks()
        
        while self.running:
            end_time        = pygame_time.get_ticks()
            dt              = (end_time - start_time) / 1000
            start_time      = end_time

            self.show_fps(dt)
            self.process_input()
            self.update(dt)
            self.draw()   
            
        pygame.quit()


