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


def get_corrected(points, surface):
    points = [Vector2(point) for point in points]

    pixels = pygame.surfarray.array2d(surface)

    topWidth = points[1][0] - points[0][0]
    bottomWidth = points[2][0] - points[3][0]
    topHeight = points[3][1] - points[0][1]
    bottomHeight = points[2][1] - points[1][1]

    CorSize = (
        int((topWidth + bottomWidth) // 2), 
        int((topHeight + bottomHeight) // 2)
    )
    CorSizeYX = (CorSize[1], CorSize[0])

    #start = perf_counter()
    x = numpy.linspace(1.0, 0.0, CorSize[0])
    y = numpy.linspace(0.0, 1.0, CorSize[1])

    yPair = numpy.repeat(y, 2).reshape(y.shape[0], 2)

    left = numpy.subtract(points[3], points[0])
    right = numpy.subtract(points[2], points[1])

    leftInterp = numpy.multiply(left, yPair) + points[0]
    rightInterp = numpy.multiply(right, yPair) + points[1]

    between = numpy.subtract(rightInterp, leftInterp)
    betweenLoc = numpy.repeat(leftInterp, x.shape[0], axis=0)
        
    #Matching array shapes by numpy.tile and repeat
    allX = numpy.tile(x, between.shape[0])
    allX = numpy.repeat(allX, 2).reshape(allX.shape[0], 2)
    allBetween = numpy.repeat(between, x.shape[0], axis=0)
    betweenPoses = numpy.multiply(allBetween, allX)
    betweenPoses = betweenPoses + betweenLoc

    xPoses = numpy.take(betweenPoses, 0, axis=1)
    yPoses = numpy.take(betweenPoses, 1, axis=1)
        
    xPoses = numpy.int_(xPoses)
    yPoses = numpy.int_(yPoses)
    
    corrected = pixels[xPoses, yPoses].reshape(CorSizeYX)
    corrected = numpy.rot90(corrected)

    surf = pygame.Surface(CorSize)
    pygame.surfarray.blit_array(surf, corrected)

    #print(perf_counter() - start)

    return surf