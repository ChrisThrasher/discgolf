import pygame
import color

from screen import screen
from circle import Circle
from vec2 import Vec2

class Slot(Circle):
    def __init__(self, pos, radius, name, color, resistance_coef, initial_height):
        super().__init__(pos, radius, color)
        self.name = name
        self.resistance_coef = resistance_coef
        self.initial_height = initial_height
    def draw(self, hover_check):
        if hover_check:
            pygame.draw.circle(screen,
                               color.LIGHT_GREY,
                               [int(self.pos.x), int(self.pos.y)],
                               int(self.radius + 5),
                               width=0)
        super().draw()
        text_surface = pygame.font.SysFont(None, 16).render(self.name, True, color.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(self.pos.x), int(self.pos.y - self.radius - 15))
        screen.blit(text_surface, text_rect)

class Bag:
    def __init__(self, slots):
        self.slots = slots
        self.selected = slots[0]
    def is_selected(self, mouse):
        for slot in self.slots:
            if mouse.overlaps(slot):
                self.selected = slot
                return True
        return False
    def draw(self, mouse):
        for slot in self.slots:
            slot.draw(mouse.overlaps(slot))

DRIVER    = Slot(Vec2(750, 50), 20, 'Driver',    color.WHITE,  0.010, 1.0)
MID_RANGE = Slot(Vec2(685, 50), 20, 'Mid Range', color.BLUE,   0.015, 0.6)
PUTTER    = Slot(Vec2(620, 50), 20, 'Putter',    color.ORANGE, 0.025, 0.1)

BAG = Bag([DRIVER, MID_RANGE, PUTTER])
