import color

from circle import Circle
from constants import *

class BagSlot(Circle):

    def __init__(self, x, y, radius, color, discType):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.r = radius
        self.color = color
        self.xc = int(x + 0.5 * radius)
        self.yc = int(y + 0.5 * radius)
        self.discType = discType
        if discType == 'Driver':
            self.resistance_coef = 0.01
        elif discType == 'Mid Range':
            self.resistance_coef = 0.015
        elif discType == 'Putter':
            self.resistance_coef = 0.02
    def text_objects(self, text, font):
        textSurface = font.render(text, True, color.WHITE)
        return textSurface, textSurface.get_rect()
    x: int
    y: int
    r: int
    color: tuple
    resistance_coef: float
    xc: int
    yc: int
    discType: str
