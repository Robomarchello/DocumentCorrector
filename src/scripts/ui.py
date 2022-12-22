#you might try using pygame_gui module for it
import pygame
from pygame.locals import *
from .mouse import Mouse

pygame.init()


class Button:
    def __init__(self, rect, font, text, textColor, 
                color, hoverColor, func, image=None):
        if image == None:
            self.rect = rect
        else:
            pass
        
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
    def __init__(self, screen):
        self.screen = screen
        size = screen.get_size()

        self.borderColor = pygame.Color(28, 28, 35)
        self.BgColor = pygame.Color(39, 39, 56)
        self.hoverColor = pygame.Color(50, 50, 70)
        self.white = pygame.Color('white')

        
        self.border = pygame.Rect(0, 0, size[0], 42)

        #9, 7
        self.icon = pygame.image.load('src/assets/logoIcon.png').convert_alpha()
        self.iconRect = self.icon.get_rect(topleft=(9, 7))
        
        self.buttonFont = pygame.font.Font('src/assets/font.ttf', 16)
        self.FileRect = pygame.Rect(50, 5, 100, 32) 
        self.ChooseFile = Button(self.FileRect, self.buttonFont, 'Choose File',
                            self.white, self.BgColor, self.hoverColor, self.load)

        self.SaveRect = pygame.Rect(160, 5, 45, 32)
        self.SaveBtn = Button(self.SaveRect, self.buttonFont, 'Save', self.white,
                              self.BgColor, self.hoverColor, self.save)

        self.CopyRect = pygame.Rect(220, 5, 137, 32)#137
        self.CopyBtn = Button(self.CopyRect, self.buttonFont, 'Copy To Clipboard',
                            self.white, self.BgColor, self.hoverColor, self.save)

    def load(self):
        print('load image, partner')

    def save(self):
        print('save image, partner')

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

class Interface:
    BgColor = pygame.Color(39, 39, 56)
    SideBarColor = pygame.Color(60, 60, 60)
    BoundColor = pygame.Color(30, 30, 30) 
    def __init__(self):
        self.surface = pygame.Surface((960, 540))

        self.Toolbar = Toolbar(self.surface)

    def draw(self, screen):
        self.surface.fill(self.BgColor)

        self.Toolbar.draw(self.surface)
        
        screen.blit(self.surface, (0, 0))

    def handle_event(self, event):
        if event.type == VIDEORESIZE:
            size = event.size
            self.surface = pygame.Surface(size)
            self.Toolbar.resize(size)

        self.Toolbar.handle_event(event)

'''
class Button:
    def __init__(self, x, y, width, height, font, text, textColor, color, mouse, func):
        self.rect = pygame.Rect(x, y, width, height)
        
        self.textRender = font.render(text, True, textColor)
        self.textRect = self.textRender.get_rect(center=self.rect.center)
        
        self.hovered = False
        self.clicked = False
        self.func = func

        self.animTime = 0
        self.animFrames = 5
        self.animPosMove = pygame.Vector2(-6, 6)

        self.color = pygame.Color(color)

        self.shadowColor = self.color.lerp((0, 0, 0), 0.2)

        self.mouse = mouse

    def draw(self, screen):
        #animation
        if self.clicked:
            if self.animTime < self.animFrames:
                self.animTime += 1
        else:
            if self.animTime > 0:
                self.animTime -= 1
        
        shadowRect = self.rect.move(-6, 6)
        pygame.draw.rect(screen, self.shadowColor, shadowRect)

        if self.animTime != 0:
            animProg = self.animTime / self.animFrames
            animRect = self.rect.move(self.animPosMove * animProg)
            self.textRect.center = animRect.center
            pygame.draw.rect(screen, self.color, animRect)

        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        screen.blit(self.textRender, self.textRect.topleft)

        if self.rect.collidepoint(self.mouse.position):
            self.hovered = True
            self.mouse.hovered = True
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
                self.clicked = False'''