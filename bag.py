import pygame
import color

from screen import screen
from circle import Circle
from constants import *
from vec2 import Vec2

class BagSlot(Circle):
    def __init__(self, pos, radius, name, color, resistance_coef):
        super().__init__(pos, radius)
        self.pos = pos
        self.r = radius
        self.color = color
        self.center = Vec2(int(pos.x + 0.5 * radius), int(pos.y + 0.5 * radius))
        self.name = name
        self.resistance_coef = resistance_coef
    def draw(self, hoverCheck):
        if hoverCheck == True:
            pygame.draw.circle(screen,
                               color.LIGHT_GREY,
                               [int(self.pos.x + 0.5 * self.r), int(self.pos.y + 0.5 * self.r)],
                               int((self.r + 10) * 0.5),
                               width=0)
        super().draw(self.color)
        textSurface = pygame.font.Font('freesansbold.ttf', 12).render(self.name, True, color.WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (int(self.pos.x + self.r * 0.5), int(self.pos.y - 15))
        screen.blit(textSurface, textRect)

DRIVER = BagSlot(Vec2(750, 50), 40, 'Driver', color.WHITE, 0.01)
MID_RANGE = BagSlot(Vec2(700, 50), 40, 'Mid Range', color.BLUE, 0.015)
PUTTER = BagSlot(Vec2(650, 50), 40, 'Putter', color.ORANGE, 0.02)

BAG = [DRIVER, MID_RANGE, PUTTER]