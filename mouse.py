import pygame

import color

from screen import screen
from vec2 import Vec2

class Mouse:
    def __init__(self):
        self.clicking = False
    def draw(self):
        if self.clicking:
            pygame.draw.line(screen, color.YELLOW, self.click_start, pygame.mouse.get_pos(), width=5)
