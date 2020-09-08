import pygame

from screen import screen
from vec2 import Vec2

class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    def draw(self, color):
        pygame.draw.ellipse(screen, color, [int(self.pos.x), int(self.pos.y), self.radius, self.radius])