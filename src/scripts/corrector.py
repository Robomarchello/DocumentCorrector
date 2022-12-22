'''
Maybe web version with file uploading?
https://pygame-web.github.io/wiki/pygbag-code/
My optional task for now is to make it realtime
'''
import pygame
from pygame.locals import *
from pygame.math import Vector2
import numpy
from time import perf_counter


class Corrector:
    def __init__(self, points, surface):
        #topleft, topright, bottomright, bottomleft
        self.points = [Vector2(point) for point in points]
        self.CorRect = pygame.Rect(0, 0, 0, 0)

        self.TargetSurf = surface
        self.pixels = numpy.array(pygame.PixelArray(surface))

        topWidth = self.points[1][0] - self.points[0][0]
        bottomWidth = self.points[2][0] - self.points[3][0]
        topHeight = self.points[3][1] - self.points[0][1]
        bottomHeight = self.points[2][1] - self.points[1][1]

        self.CorSize = (
            int((topWidth + bottomWidth) // 2), 
            int((topHeight + bottomHeight) // 2)
        )
        self.CorSizeYX = (self.CorSize[1], self.CorSize[0])
        self.viewSize = []
        
        start = perf_counter()
        x = numpy.linspace(1.0, 0.0, self.CorSize[0])
        y = numpy.linspace(0.0, 1.0, self.CorSize[1])

        diff1 = numpy.subtract(self.points[3], self.points[0])
        leftX = numpy.multiply(diff1[0], y) + self.points[0][0]
        leftY = numpy.multiply(diff1[1], y) + self.points[0][1]

        diff2 = numpy.subtract(self.points[2], self.points[1])
        rightX = numpy.multiply(diff2[0], y) + self.points[1][0]
        
        leftForX = numpy.repeat(leftX, x.shape[0])

        diffX = numpy.subtract(rightX, leftX)
        AllDiff = numpy.repeat(diffX, x.shape[0])
        AllX = numpy.tile(x, y.shape[0])

        xPoses = numpy.multiply(AllX, AllDiff) + leftForX
        yPoses = numpy.repeat(leftY, x.shape[0])
        
        xPoses = numpy.int_(xPoses)
        yPoses = numpy.int_(yPoses)

        self.corrected = self.pixels[xPoses, yPoses].reshape(self.CorSizeYX)
        self.corrected = numpy.rot90(self.corrected)

        print(perf_counter() - start)

        #self.surf = pygame.surfarray.make_surface(self.corrected)
        self.surf = pygame.Surface(self.CorSize)

        #This was/can be used for some debugging
        #self.arr = numpy.array([yPoses, xPoses]).T

    def draw(self, screen):
        pygame.surfarray.blit_array(self.surf, self.corrected)
        screen.blit(self.surf, (0, 0))#(204, 100))