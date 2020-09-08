import color

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

DRIVER = BagSlot(Vec2(750, 50), 40, 'Driver', color.WHITE, 0.01)
MID_RANGE = BagSlot(Vec2(700, 50), 40, 'Mid Range', color.BLUE, 0.015)
PUTTER = BagSlot(Vec2(650, 50), 40, 'Putter', color.ORANGE, 0.02)

BAG = [DRIVER, MID_RANGE, PUTTER]