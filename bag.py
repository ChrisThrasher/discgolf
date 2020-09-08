import pygame
import color

from screen import screen
from circle import Circle
from vec2 import Vec2

class BagSlot(Circle):
    def __init__(self, pos, radius, name, color, resistance_coef):
        super().__init__(pos, radius, color)
        self.name = name
        self.resistance_coef = resistance_coef
    def draw(self, hoverCheck):
        if hoverCheck == True:
            pygame.draw.circle(screen,
                               color.LIGHT_GREY,
                               [int(self.pos.x), int(self.pos.y)],
                               int(self.radius + 5),
                               width=0)
        super().draw()
        textSurface = pygame.font.Font('freesansbold.ttf', 12).render(self.name, True, color.WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (int(self.pos.x), int(self.pos.y - self.radius - 15))
        screen.blit(textSurface, textRect)

DRIVER = BagSlot(Vec2(750, 50), 20, 'Driver', color.WHITE, 0.01)
MID_RANGE = BagSlot(Vec2(685, 50), 20, 'Mid Range', color.BLUE, 0.015)
PUTTER = BagSlot(Vec2(620, 50), 20, 'Putter', color.ORANGE, 0.02)

BAG = [DRIVER, MID_RANGE, PUTTER]