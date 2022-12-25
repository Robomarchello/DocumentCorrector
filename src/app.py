import pygame
from pygame.locals import *
from .scripts.corrector import Corrector
from .scripts.ui import Interface
from .scripts.mouse import Mouse

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize, RESIZABLE)
        pygame.display.set_caption(caption)

        self.surface = pygame.image.load('src/assets/distorted.png').convert()
        self.copy = self.surface.copy()

        self.interface = Interface()

        #topleft, topright, bottomright, bottomleft
        points = [[205, 100], [565, 100], [765, 690], [5, 690]]
        #[[204, 100], [567, 100], [763, 690], [4, 690]]
        ##[[10, 211], [1024, 32], [1200, 990], [248, 1233]]
        #self.corrector = Corrector(points, self.surface)

        self.Debug = False

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.event_handlers = [Mouse, self.interface]

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            #UNCOMMENT WHEN DONE WITH UI
            #self.corrector.draw(screen)
            #if self.Debug:
            #    self.screen.blit(self.copy, (0, 0))

            self.interface.draw(screen)
            

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == KEYDOWN:
                    if self.Debug:
                        self.Debug = False
                    else:
                        self.Debug = True

                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            Mouse.update()
            pygame.display.update()