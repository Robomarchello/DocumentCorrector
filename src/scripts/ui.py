import pygame
from pygame.locals import *

pygame.init()


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
                self.clicked = False


class Viewport:
    def __init__(self):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass


class Interface:
    DarkGrey = pygame.Color(75, 75, 75)
    SideBarColor = pygame.Color(60, 60, 60)
    BoundColor = pygame.Color(30, 30, 30) 
    def __init__(self, mouse):
        self.mouse = mouse
        self.surface = pygame.Surface((960, 540))
        
        self.SideBar = pygame.Rect(700, 0, 260, 540)
        self.SideBarBound = pygame.Rect(695, 0, 5, 540)

        self.font = pygame.font.Font('src/assets/font.ttf', 48)
        self.SelectBtn = Button(720, 350, 230, 70, self.font, 'Select File',
        (30, 30, 30), (65, 65, 65), self.mouse, self.function)

        self.CorrectBtn = Button(720, 450, 230, 70, self.font, 'Correct It',
        (30, 30, 30), (12, 100, 70), self.mouse, self.function)

        self.Viewport = Viewport()

    def function(self):
        print('Slava Ukraini!')

    def draw(self, screen):
        self.surface.fill(self.DarkGrey)
        pygame.draw.rect(self.surface, self.SideBarColor, self.SideBar)

        self.SelectBtn.draw(self.surface)
        self.CorrectBtn.draw(self.surface)

        pygame.draw.rect(self.surface, self.BoundColor, self.SideBarBound)
        
        screen.blit(self.surface, (0, 0))

    def handle_event(self, event):
        self.SelectBtn.handle_event(event)
        self.CorrectBtn.handle_event(event)