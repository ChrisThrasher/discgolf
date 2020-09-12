import pygame
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
    def get_pos(self):
        return Vec2.from_tuple(pygame.mouse.get_pos())
    def down(self):
        self.clicking = True
        self.click_start = self.get_pos()
    def up(self):
        self.clicking = False
    def overlaps(self, circle):
        return (self.pos - circle.pos).norm() <= circle.radius
    def draw(self):
        if self.clicking:
            throw_vec_mag = (self.get_pos() - self.click_start).norm()
            colorGradientIdx = throw_vec_mag / self.max_draw_length
            if colorGradientIdx >= 1:
                colorGradientIdx = 1
                mouse_pos_hat = (self.get_pos() - self.click_start) / throw_vec_mag
                mouse_pos = self.click_start + mouse_pos_hat * self.max_draw_length
            else:
                mouse_pos = self.get_pos()
            self.relative_throw_vec = mouse_pos - self.click_start
            colorGradient = color.colorFader(color.YELLOW, color.RED, colorGradientIdx)
            pygame.draw.line(screen, colorGradient, [self.click_start.x, self.click_start.y], [mouse_pos.x, mouse_pos.y], width=5)
