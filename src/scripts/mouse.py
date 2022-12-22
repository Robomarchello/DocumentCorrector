import pygame
from pygame.locals import *


class Mouse:
    position = pygame.Vector2(0, 0)
    hovered = False
    resize = False

    @classmethod
    def update(cls):
        if cls.hovered:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
        elif cls.resize:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_SIZEWE)        
        else:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)

        cls.resize = False
        cls.hovered = False

    @classmethod
    def handle_event(cls, event):
        if event.type == MOUSEMOTION:
            cls.position.update(event.pos)