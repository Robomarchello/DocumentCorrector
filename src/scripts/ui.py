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


class ViewPort:
    def __init__(self):
        pass


class Interface:
    def __init__(self, mouse):
        self.mouse = mouse
        self.surface = pygame.Surface((960, 540))
        
        self.font = pygame.font.Font('src/assets/font.ttf', 48)
        self.Button = Button(350, 250, 215, 70, self.font, 'Select',
        (30, 30, 30), (12, 100, 70), self.mouse, self.function)

    def function(self):
        print('Slava Ukraini!')

    def draw(self, screen):
        self.surface.fill((75, 75, 75))
        
        self.Button.draw(self.surface)

        screen.blit(self.surface, (0, 0))

    def handle_event(self, event):
        self.Button.handle_event(event)