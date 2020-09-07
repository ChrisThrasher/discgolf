import pygame

from screen import screen
from vec2 import Vec2

class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    def center(self):
        return self.pos + Vec2(self.radius, self.radius)
    def draw(self, color):
        pygame.draw.circle(screen, color, [int(self.center().x), int(self.center().y)], self.radius)