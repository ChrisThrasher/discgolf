import color

from circle import Circle
from constants import *

class BagSlot(Circle):
    def __init__(self, pos, radius, color, discType):
        super().__init__(pos, radius)
        self.pos = pos
        self.r = radius
        self.color = color
        self.xc = int(pos.x + 0.5 * radius)
        self.yc = int(pos.y + 0.5 * radius)
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
    r: int
    color: tuple
    resistance_coef: float
    xc: int
    yc: int
    discType: str
