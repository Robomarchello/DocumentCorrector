import pygame
from pygame.locals import *
from .scripts.corrector import Corrector

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.surface = pygame.image.load('src/assets/distorted.png').convert()
        self.cpy = self.surface.copy()

        #topleft, topright, bottomright, bottomleft
        points = [[204, 100], [567, 100], [763, 690], [4, 690]]
        self.corrector = Corrector(points, self.surface)

        self.Debug = False

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            self.corrector.draw(screen)
            if self.Debug:
                self.screen.blit(self.cpy, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == KEYDOWN:
                    if self.Debug:
                        self.Debug = False
                    else:
                        self.Debug = True
            pygame.display.update()