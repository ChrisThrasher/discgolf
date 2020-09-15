import numpy as np
import pygame

import color

from screen import screen
from circle import Circle
from vec2 import Vec2

class Wind(Circle):
    def __init__(self, pos, radius, max_speed):
        super().__init__(pos, radius, color.LIGHT_GREY)
        self.speed = np.random.rand() * max_speed
        self.heading = np.deg2rad(np.random.randint(360))
        self.vel = Vec2(np.cos(self.heading), np.sin(self.heading)) * self.speed
    def draw(self):
        super().draw()
        start_pos = self.pos
        end_pos = self.pos + Vec2(np.cos(self.heading), np.sin(self.heading)) * self.radius
        pygame.draw.line(screen, color.WHITE, start_pos.as_tuple(), end_pos.as_tuple(), width=5)
        text = ('Wind Speed: ' + str(round(self.speed, 1)))
        text_surf = pygame.font.SysFont(None, 24).render(text, True, color.WHITE)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(self.pos.x), int(self.pos.y - self.radius - 15))
        screen.blit(text_surf, text_rect)
    speed: float = 0.0
    heading: float = 0.0
