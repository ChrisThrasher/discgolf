import pygame

from screen import screen
from vec2 import Vec2

class Circle:
    def __init__(self, pos, radius, color):
        self.pos = pos
        self.radius = radius
        self.color = color
    def draw(self):
        pygame.draw.circle(screen, self.color, [int(self.pos.x), int(self.pos.y)], self.radius)
