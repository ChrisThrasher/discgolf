import pygame
from numpy import linalg as LA
import numpy as np
import color

from screen import screen
from vec2 import Vec2

class Mouse:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.clicking = False
        self.click_start = Vec2(0, 0)
        self.max_draw_length = 250
        self.relative_throw_vec = Vec2(0, 0)
    def down(self):
        self.clicking = True
        self.click_start = pygame.mouse.get_pos()
    def up(self):
        self.clicking = False
    def overlaps(self, circle):
        return (self.pos - circle.pos).norm() <= circle.radius
    def draw(self):
        if self.clicking:
            throw_vec_mag = LA.norm(np.subtract(pygame.mouse.get_pos(), self.click_start))
            colorGradientIdx = throw_vec_mag / self.max_draw_length
            if colorGradientIdx >= 1:
                colorGradientIdx = 1
                mouse_pos_hat    = np.subtract(pygame.mouse.get_pos(), self.click_start) / throw_vec_mag
                mouse_pos        = tuple([self.click_start[nt] + x * self.max_draw_length for nt, x in enumerate(mouse_pos_hat)])
            else:
                mouse_pos = pygame.mouse.get_pos()
            self.relative_throw_vec = tuple(np.subtract(mouse_pos, self.click_start))
            colorGradient = color.colorFader(color.YELLOW, color.RED, colorGradientIdx)
            pygame.draw.line(screen, colorGradient, self.click_start, mouse_pos, width=5)
