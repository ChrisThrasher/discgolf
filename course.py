import pygame

import color

from screen import screen

def DrawHole1():
    screen.fill(color.GREEN)
    pygame.draw.ellipse(screen, color.LIGHT_GREEN, [340, 100, 120, 400])
    pygame.draw.rect(screen, color.LIGHT_GREY, [390, 480, 20, 50])

class Course:
    def __init__(self):
        self.current_hole = 1
        self.holes = {1 : DrawHole1}
    def next_hole(self):
        self.current_hole = self.current_hole + 1
        return self.current_hole <= len(self.holes)
    def draw(self):
        self.holes[self.current_hole]()
