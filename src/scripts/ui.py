import pygame
import pygame.scrap
from pygame.locals import *
from .mouse import Mouse
from .corrector import get_corrected
from math import sqrt
import json
from os import path

pygame.init()


class Alert:
    def __init__(self, text, color, frames):
        pass

    def draw(self, screen):
        pass


class Button:
    def __init__(self, rect, font, text, textColor, 
                color, hoverColor, func):
        self.rect = rect
        
        self.textRender = font.render(text, True, textColor)
        self.textRect = self.textRender.get_rect(center=self.rect.center)
        
        self.hovered = False
        self.clicked = False
        self.func = func

        self.color = pygame.Color(color)
        self.hoverColor = pygame.Color(hoverColor)
        self.borderColor = self.hoverColor.lerp((255, 255, 255), 0.1)

    def draw(self, screen):
        if self.hovered:
            pygame.draw.rect(screen, self.hoverColor, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        screen.blit(self.textRender, self.textRect.topleft)

        if self.rect.collidepoint(Mouse.position):
            self.hovered = True
            Mouse.hovered = True
        else:
            self.hovered = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.func()
                    self.clicked = True
        
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False


class Toolbar:
    def __init__(self, screen, editor):
        self.screen = screen
        size = screen.get_size()

        self.borderColor = pygame.Color(28, 28, 35)
        self.BgColor = pygame.Color(39, 39, 56)
        self.hoverColor = pygame.Color(50, 50, 70)
        self.white = pygame.Color('white')

        self.border = pygame.Rect(0, 0, size[0], 42)

        self.icon = pygame.image.load('src/assets/logoIcon.png').convert_alpha()
        self.iconRect = self.icon.get_rect(topleft=(9, 7))
        
        self.buttonFont = pygame.font.Font('src/assets/font.ttf', 16)
        self.FileRect = pygame.Rect(50, 5, 38, 32) 
        self.ChooseFile = Button(self.FileRect, self.buttonFont, 'Load',
                            self.white, self.BgColor, self.hoverColor, self.load)

        self.SaveRect = pygame.Rect(103, 5, 45, 32)
        self.SaveBtn = Button(self.SaveRect, self.buttonFont, 'Save', self.white,
                              self.BgColor, self.hoverColor, self.save)

        self.CopyRect = pygame.Rect(163, 5, 40, 32)#137
        self.CopyBtn = Button(self.CopyRect, self.buttonFont, 'Copy',
                            self.white, self.BgColor, self.hoverColor, self.copy)

        self.editor = editor

    def load(self):
        print('load image, partner')

    def save(self):
        self.editor.SaveOutput('corrected.png')

        print('Output Saved!')

    def copy(self):
        self.editor.SaveOutput('src/assets/ToClipboard.bmp')

        with open('src/assets/ToClipboard.bmp', 'rb') as file:
            pygame.scrap.put(SCRAP_BMP, file.read())

        print('Copied!')

    def resize(self, size):
        self.border.width = size[0]
        
    def draw(self, screen):
        pos = [self.border.bottomleft, self.border.bottomright]
        pygame.draw.rect(screen, self.BgColor, self.border)

        screen.blit(self.icon, self.iconRect.topleft)

        self.ChooseFile.draw(screen)
        self.SaveBtn.draw(screen)
        self.CopyBtn.draw(screen)

        pygame.draw.rect(screen, self.borderColor, self.border, width=2)
        pygame.draw.line(screen, self.borderColor, pos[0], pos[1], 4)

    def handle_event(self, event):
        self.ChooseFile.handle_event(event)
        self.SaveBtn.handle_event(event)
        self.CopyBtn.handle_event(event)


class Point:
    def __init__(self, position, size, boundRect):
        self.position = pygame.Vector2(position)
        self.OriginPos = self.position - boundRect.topleft
        
        self.size = size

        self.boundRect = boundRect

        self.radius = 12
        
        self.orange = pygame.Color(255, 145, 100)
        self.grey = pygame.Color(50, 50, 65)

        self.pressed = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.grey, self.position, self.radius)
        pygame.draw.circle(screen, self.orange, self.position, self.radius, 3)

    def update(self):
        if self.pressed:
            self.position = Mouse.position.copy()
            self.OriginPos = self.position - self.boundRect.topleft

            self.BoundCheck()

    def BoundCheck(self):
        '''
        Checking if point position is less than bound
        '''
        if self.position[0] < self.boundRect.left:
            self.position[0] = self.boundRect.left
        
        elif self.position[0] > self.boundRect.right:
            self.position[0] = self.boundRect.right

        if self.position[1] < self.boundRect.top:
            self.position[1] = self.boundRect.top
        
        elif self.position[1] > self.boundRect.bottom:
            self.position[1] = self.boundRect.bottom

        self.OriginPos = self.position - self.boundRect.topleft

    def updateBound(self, boundRect):
        diffX = ((boundRect.width + 0.01) / (self.boundRect.width + 0.01))
        diffY = ((boundRect.height + 0.01) / (self.boundRect.height + 0.01))

        self.OriginPos = self.scale(self.boundRect)

        self.boundRect = boundRect

        self.OriginPos[0] *= diffX
        self.OriginPos[1] *= diffY

        self.position = self.OriginPos + self.boundRect.topleft

    def scaleCheck(self, OriginPos, rect):
        '''
        function made specifically for self.scale
        so i can get away without errors😳
        did - 1 so the indecies are right
        '''
        if OriginPos[0] < 0:
            OriginPos[0] = 0

        if OriginPos[1] < 0:
            OriginPos[1] = 0

        if OriginPos[0] >= rect.width:
            OriginPos[0] = rect.width - 1

        if OriginPos[1] >= rect.height:
            OriginPos[1] = rect.height - 1

        return OriginPos

    def scale(self, rect, scaleCheck=False):
        # doing + 0.01 so i don't get 0 division error💀
        diffX = ((rect.width + 0.01) / (self.boundRect.width + 0.01))
        diffY = ((rect.height + 0.01) / (self.boundRect.height + 0.01))

        OriginPos = pygame.Vector2(self.OriginPos[0] * diffX, self.OriginPos[1] * diffY)
        if scaleCheck:
            OriginPos = self.scaleCheck(OriginPos, rect)

        return OriginPos
        
    def collide(self):
        mousePos = Mouse.position
        diff = sqrt(
            (self.position[0] - mousePos[0]) ** 2 +
            (self.position[1] - mousePos[1]) ** 2)
        
        if diff - self.radius < 0:
            return True
        
        return False

    def handle_event(self, event, points):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.collide():
                    pressable = True
                    for point in points:
                        if point.pressed:
                            pressable = False
                    if pressable:
                        self.pressed = True

        if event.type == MOUSEBUTTONUP:
            self.pressed = False


class Editor:
    def __init__(self, ScreenSize):
        #initializing here because pygame.scrap requires window
        pygame.scrap.init()

        self.ScreenSize = ScreenSize
        self.HalfSize = (ScreenSize[0] // 2, ScreenSize[1] // 2)

        self.borderColor = pygame.Color(28, 28, 41)

        self.surf = pygame.image.load('src/assets/template.png').convert()
        self.OutputSurf = self.surf.copy()

        self.errorSurf = pygame.image.load('src/assets/error.png').convert()
        self.errorRect = self.errorSurf.get_rect()

        self.resolution = pygame.Rect(0, 0, 768, 768)
        ResDict = {'resolution': self.resolution.size}

        if path.isfile('config.json'):
            with open('config.json', 'r') as config:
                ResDict = json.load(config)
                self.resolution.size = ResDict['resolution']
        else:
            with open('config.json', 'w') as config:
                json.dump(ResDict, config)


        #Scaling image to self.resolution to size to work at higher fps
        self.TransRect = self.surf.get_rect().fit(self.resolution)
        self.scaledSurf = pygame.transform.scale(self.surf, self.TransRect.size)

        self.surfRect1 = self.surf.get_rect()
        self.surfRect2 = self.OutputSurf.get_rect()

        self.leftRect = pygame.Rect(0, 45, self.HalfSize[0], 499)
        self.rightRect = pygame.Rect(self.HalfSize[0], 45, self.HalfSize[0], 499)

        self.divider = pygame.Rect(self.HalfSize[0], 45, 6, 499)
        self.hovered = False
        self.pressed = False
        self.firstTime = True

        self.moveDivider(Mouse.position[0])
        
        offset = [self.fitLeftRect.width * 0.1, self.fitLeftRect.height * 0.1]
        pointRect = self.fitLeftRect.move(offset)
        pointRect.size = (pointRect.width - offset[0] * 2,
                          pointRect.height - offset[1] * 2) 

        self.points = [
            Point(pointRect.topleft, self.ScreenSize, self.fitLeftRect),
            Point(pointRect.topright, self.ScreenSize, self.fitLeftRect),
            Point(pointRect.bottomright, self.ScreenSize, self.fitLeftRect),
            Point(pointRect.bottomleft, self.ScreenSize, self.fitLeftRect)
            ]

        self.polySurf = pygame.Surface(self.fitLeftRect.size, SRCALPHA)
        self.polySurf.set_alpha(127)
        
        self.updateOutput()

    def updateOutput(self):
        '''
        Getting corrected surface and setting it as OutputSurf
        '''
        positions = []
        for point in self.points:
            positions.append(point.scale(self.TransRect, True))

        try:
            self.OutputSurf = get_corrected(positions, self.scaledSurf)
        except:
            self.OutputSurf = self.errorSurf

        self.updateScaledSurf()

    def SaveOutput(self, path):
        '''
        Saves corrected image in the original resolution
        '''
        positions = []
        for point in self.points:
            positions.append(point.scale(self.surfRect1, True))

        try:
            corrected = get_corrected(positions, self.surf)
            pygame.image.save(corrected, path)
        except:
            print('error correcting the image')

    def LoadImage(self, path):
        self.surf = pygame.image.load(path).convert()#.convert_alpha()
        self.TransRect = self.surf.get_rect().fit(self.resolution)
        self.scaledSurf = pygame.transform.scale(self.surf, self.TransRect.size)

        self.updateOutput()

    def draw(self, screen):
        if self.divider.collidepoint(Mouse.position):
            self.hovered = True
            Mouse.resize = True
        else:
            self.hovered = False

        if self.pressed:
            self.moveDivider(Mouse.position[0])

        screen.blit(self.SurfScaled, self.fitLeftRect.topleft)
        screen.blit(self.OutputScaled, self.fitRightRect.topleft)

        positions = []
        update = False
        for point in self.points:
            point.update()
            point.updateBound(self.fitLeftRect)

            if point.pressed:
                update = True

            positions.append(point.OriginPos)

        if update:
            self.updateOutput()

        self.polySurf.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.polySurf, (200, 200, 200), positions)
        screen.blit(self.polySurf, self.fitLeftRect.topleft)

        #i made another loop for drawing so points are above the polygon
        for point in self.points:
            point.draw(screen)

        position1 = (self.divider.centerx, 45)
        position2 = (self.divider.centerx, self.ScreenSize[1])
        pygame.draw.line(screen, self.borderColor, position1, position2, 5)

    def moveDivider(self, xPos):
        Mouse.resize = True
        if self.firstTime:
            self.divider.centerx = self.HalfSize[0]
            self.firstTime = False
        else:
            self.divider.centerx = xPos
            self.divider.height = self.ScreenSize[1]

            self.leftRect.width = xPos
            self.rightRect.x = xPos
            self.rightRect.width = self.ScreenSize[0] - xPos

        self.fitLeftRect = self.surfRect1.fit(self.leftRect)
        self.fitRightRect = self.surfRect2.fit(self.rightRect)

        self.polySurf = pygame.Surface(self.fitLeftRect.size, SRCALPHA)
        self.polySurf.set_alpha(127)

        self.updateScaledSurf()

    def updateScaledSurf(self):
        self.surfRect1 = self.surf.get_rect()
        self.surfRect2 = self.OutputSurf.get_rect()

        if self.surfRect2.size == (0, 0):
            #handling 0 size error
            self.OutputSurf = self.errorSurf
            self.surfRect2 = self.errorRect  

        self.fitLeftRect = self.surfRect1.fit(self.leftRect)
        self.fitRightRect = self.surfRect2.fit(self.rightRect)

        self.SurfScaled = pygame.transform.scale(self.surf, self.fitLeftRect.size)
        self.OutputScaled = pygame.transform.scale(self.OutputSurf, self.fitRightRect.size)

    def resize(self, size):
        self.ScreenSize = size
        self.HalfSize = (size[0] // 2, size[1] // 2)

        self.divider.centerx = self.HalfSize[0]
        self.leftRect.size = (self.HalfSize[0], self.ScreenSize[1] - 45)
        self.rightRect.x = self.HalfSize[0]
        self.rightRect.size = (self.HalfSize[0], self.ScreenSize[1] - 45)

        self.moveDivider(self.HalfSize[0])

        self.divider.centerx = self.HalfSize[0]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.pressed = True

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.pressed = False

        for point in self.points:
            point.handle_event(event, self.points)

        if event.type == DROPFILE:
            self.LoadImage(event.file)
            

class Interface:
    BgColor = pygame.Color(39, 39, 56)
    def __init__(self):
        self.size = (960, 540)
        self.surface = pygame.Surface(self.size)

        self.Editor = Editor(self.size)
        self.Toolbar = Toolbar(self.surface, self.Editor)

    def draw(self, screen):
        self.surface.fill(self.BgColor)

        self.Toolbar.draw(self.surface)
        self.Editor.draw(self.surface)
        
        screen.blit(self.surface, (0, 0))

    def handle_event(self, event):
        if event.type == VIDEORESIZE:
            self.size = event.size
            self.surface = pygame.Surface(self.size)
            self.Toolbar.resize(self.size)
            self.Editor.resize(self.size)

        self.Editor.handle_event(event)
        self.Toolbar.handle_event(event)
