'''
Maybe web version with file uploading?
https://pygame-web.github.io/wiki/pygbag-code/
'''
import pygame
from pygame.locals import *
from pygame.math import Vector2
import numpy


class Corrector:
    def __init__(self, points, surface):
        #topleft, topright, bottomright, bottomleft
        self.points = [Vector2(point) for point in points]
        self.CorRect = pygame.Rect(0, 0, 0, 0)

        self.TargetSurf = surface
        self.pixels = pygame.PixelArray(surface)

        topWidth = self.points[1][0] - self.points[0][0]
        bottomWidth = self.points[2][0] - self.points[3][0]
        topHeight = self.points[3][1] - self.points[0][1]
        bottomHeight = self.points[2][1] - self.points[1][1]

        self.CorSize = (
            int((topWidth + bottomWidth) // 2), 
            int((topHeight + bottomHeight) // 2)
        )

        maxSize = (960, 540)
        self.viewSize = []

        self.corrected = pygame.PixelArray(pygame.Surface(self.CorSize))
        self.interpPoses = numpy.zeros((self.CorSize), list)
        for y in range(self.CorSize[1]):
            for x in range(self.CorSize[0]):
                interpX = x / self.CorSize[0]
                interpY = 1 - y / self.CorSize[1]
        
                line = [
                self.points[3].lerp(self.points[0], interpY),
                self.points[2].lerp(self.points[1], interpY)
                ]
                point = line[0].lerp(line[1], interpX)

                self.corrected[x][y] = self.pixels[int(point[0])][int(point[1])]


    def draw(self, screen):
        surf = self.corrected.make_surface()
        screen.blit(surf, (0, 0))