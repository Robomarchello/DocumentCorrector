#plan it out, rewrite
import pygame
from pygame.locals import *
from pygame.math import Vector2
import numpy


class Corrector:
    def __init__(self, points, surface):
        #topleft, topright, bottomright, bottomleft
        #[79, 47], [522, 82], [688, 721], [245, 681]
        self.points = [Vector2(point) for point in points]
        self.CorRect = pygame.Rect(0, 0, 0, 0)

        self.TargetSurf = surface
        self.pixels = pygame.PixelArray(surface)

        #Corrected points
        xDiff = (self.points[3][0] - self.points[0][0]) // 2
        yDiff = (self.points[1][1] - self.points[0][1]) // 2
        
        top = self.points[0][1] + yDiff
        left = self.points[0][0] + xDiff
        bottom = self.points[3][1] + yDiff
        right = self.points[1][0] + xDiff 
        self.CorRect = pygame.Rect(left, top, bottom - top, right - left)
        self.corrected = pygame.PixelArray(pygame.Surface(self.CorRect.size))

        self.interpPoses = numpy.zeros((self.CorRect.size), list)
        
        for y in range(self.CorRect.height):
            for x in range(self.CorRect.width):
                interpX = x / self.CorRect.width
                interpY = 1 - (y / self.CorRect.height)
        
                line = [
                self.points[3].lerp(self.points[0], interpY),
                self.points[2].lerp(self.points[1], interpY)
                ]
                point = line[0].lerp(line[1], interpX)

                self.corrected[x][y] = self.pixels[int(point[0])][int(point[1])]


    def draw(self, screen):
        surf = self.corrected.make_surface()
        screen.blit(surf, (0, 0))