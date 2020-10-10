import pygame
import os
import numpy as np
import color
import numpy as np

from circle import Circle
from screen import screen
from vec2 import Vec2

class Basket(Circle):
    def __init__(self, pos):
        super().__init__(pos, 10, color.GREY)

class Tree(Circle):
    def __init__(self, pos, radius=8):
        super().__init__(pos, radius, color.DARK_GREEN)

class Tee:
    def __init__(self, pos):
        self.pos = pos
        self.width = 20
        self.height = 50
        self.image = pygame.image.load(os.path.join("assets", "Tee.png"))
    def center(self):
        return self.pos + Vec2(self.width / 2, self.height / 2)
    def draw(self):
        screen.blit(self.image, self.pos.as_tuple())

class Hole:
    def __init__(self, background, tee, basket, trees):
        self.background = pygame.image.load(os.path.join("assets", background))
        self.tee = tee
        self.trees = trees
        self.basket = basket
        self.stroke_count = 0
    def check_collision(self,disc):
        cp = disc.pos
        r  = disc.radius
        xx = np.linspace(cp.x - r,cp.x + r,2*r + 1)
        yy = np.linspace(cp.y - r,cp.y + r,2*r + 1)
        for x in xx:
            for y in yy:
                point = Vec2(x,y)
                if (disc.pos - point).norm() <= (disc.radius):
                    rgb_under_disc = screen.get_at((int(x),int(y)))[:3]
                    if rgb_under_disc == color.DARK_GREEN:
                        disc.stop()
    def reset(self, disc):
        disc.pos = self.tee.pos
    def throw(self):
        self.stroke_count += 1
    def draw(self):
        screen.blit(self.background, (0, 0))
        self.tee.draw()
        for tree in self.trees:
            tree.draw()
        self.basket.draw()

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

class Course:
    def __init__(self, holes):
        self.current_hole = 0
        self.holes = holes
        self.wind = Wind(Vec2(100, 100), 50, max_speed=50)
    def hole(self):
        return self.holes[self.current_hole]
    def next_hole(self):
        print(f"Completed hole {self.current_hole + 1} in {self.hole().stroke_count} strokes.")
        self.current_hole += 1
        return self.current_hole < len(self.holes)
    def draw(self):
        self.holes[self.current_hole].draw()
        self.wind.draw()

HOLE1 = Hole("Hole1.png", Tee(Vec2(390, 480)), Basket(Vec2(440, 160)), [Tree(Vec2(450, 110)),
                                                                        Tree(Vec2(400, 100)),
                                                                        Tree(Vec2(350, 120)),
                                                                        Tree(Vec2(490, 140)),
                                                                        Tree(Vec2(455, 210)),
                                                                        Tree(Vec2(400, 350))])

HOLE2 = Hole("Hole2.png", Tee(Vec2(390, 480)), Basket(Vec2(225, 120)), [Tree(Vec2(265, 200)),
                                                                        Tree(Vec2(255, 240)),
                                                                        Tree(Vec2(310, 265)),
                                                                        Tree(Vec2(310, 335))])

HOLE3 = Hole("Hole3.png", Tee(Vec2(280, 480)), Basket(Vec2(530, 140)), [Tree(Vec2(450, 190)),
                                                                        Tree(Vec2(385, 300)),
                                                                        Tree(Vec2(390, 230)),
                                                                        Tree(Vec2(355, 425)),
                                                                        Tree(Vec2(350, 470)),
                                                                        Tree(Vec2(350, 385))])

COURSE = Course([HOLE1, HOLE2, HOLE3])
