import pygame
from numpy import linalg as LA
import numpy as np
import color
import matplotlib as mpl

from screen import screen
from vec2 import Vec2

class Mouse:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.clicking = False
        self.click_start = Vec2(0, 0)
        self.max_draw_length = 300
    def down(self):
        self.clicking = True
        self.click_start = pygame.mouse.get_pos()
    def up(self):
        self.clicking = False
    def overlaps(self, circle):
        return (self.pos - circle.pos).norm() <= circle.radius
    def draw(self):
        if self.clicking:
            # pygame.draw.line(screen, color.YELLOW, self.click_start, pygame.mouse.get_pos(), width=5)
            temp = LA.norm(np.subtract(pygame.mouse.get_pos(),self.click_start))
            colorGradientIdx = temp/self.max_draw_length
            if colorGradientIdx >= 1:
                colorGradientIdx = 1
            c1 = '#ffff00'
            c2 = '#ff0000'
            colorGradient = tuple([255*x for x in mpl.colors.to_rgb(color.colorFader(c1,c2,colorGradientIdx))])
            pygame.draw.line(screen, colorGradient, self.click_start, pygame.mouse.get_pos(), width=5)
