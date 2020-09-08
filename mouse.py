import pygame

import color

from screen import screen
from vec2 import Vec2

class Mouse:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.clicking = False
    def down(self):
        self.clicking = True
        pygame.mouse.get_rel()
        self.click_start = pygame.mouse.get_pos()
    def up(self):
        self.clicking = False
    def overlaps(self, circle):
        return (self.pos - circle.pos).norm() <= circle.radius
    def draw(self):
        if self.clicking:
            pygame.draw.line(screen, color.YELLOW, self.click_start, pygame.mouse.get_pos(), width=5)
