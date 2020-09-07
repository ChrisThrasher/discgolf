import numpy as np
import pygame

import color

from screen import screen
from circle import Circle
from vec2 import Vec2

class Wind(Circle):
    def __init__(self, x, y, radius, max_speed):
        super().__init__(Vec2(x, y), radius)
        self.speed = np.random.rand() * max_speed
        self.heading = np.deg2rad(np.random.randint(360))
        self.vel = Vec2(np.cos(self.heading), np.sin(self.heading)) * self.speed
    def text_objects(self, text, font):
        text_surface = font.render(text, True, color.WHITE)
        return text_surface, text_surface.get_rect()
    def draw(self):
        super().draw(color.LIGHT_GREY)
        start_pos = self.center()
        end_pos = self.center() + Vec2(np.cos(self.heading), np.sin(self.heading)) * self.radius * 0.5
        pygame.draw.line(screen, color.WHITE, start_pos.as_tuple(), end_pos.as_tuple(), width=5)
        wind_speed_text = pygame.font.Font('freesansbold.ttf', 16)
        text = ('Wind Speed: ' + str(round(self.speed, 1)))
        text_surf, text_rect = self.text_objects(text, wind_speed_text)
        text_rect.center = (int(self.pos.x + self.radius * 0.5), int(self.pos.y - 15))
        screen.blit(text_surf, text_rect)
    speed: float = 0.0
    heading: float = 0.0