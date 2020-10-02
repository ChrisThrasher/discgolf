import pygame

import color
import numpy as np

from circle import Circle
from screen import screen
from vec2 import Vec2

class Fairway:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height
    def draw(self):
        pygame.draw.ellipse(screen, color.LIGHT_GREEN, [self.pos.x, self.pos.y, self.width, self.height])

class Tee:
    def __init__(self, pos):
        self.pos = pos
        self.width = 20
        self.height = 50
    def center(self):
        return self.pos + Vec2(self.width / 2, self.height / 2)
    def draw(self):
        pygame.draw.rect(screen, color.LIGHT_GREY, [self.pos.x, self.pos.y, self.width, self.height])

class Hole:
    def __init__(self, fairway, tee, trees, basket):
        self.fairway = fairway
        self.tee = tee
        self.trees = trees
        self.basket = basket
    def check_collision(self, disc):
        for tree in self.trees:
            if disc.hit(tree):
                tree_to_disc = disc.pos - tree.pos
                direction = tree_to_disc / tree_to_disc.norm()
                disc.pos = direction * (tree.radius + disc.radius + 5) + tree.pos
                disc.stop()

    def check_collision_new(self,disc):
        cp = disc.pos
        r = disc.radius
        xx = np.linspace(cp.x - r,cp.x + r,2*r + 1)
        yy = np.linspace(cp.y - r,cp.y + r,2*r + 1)
        for x in xx:
            for y in yy:
                point = Vec2(x,y)
                if (disc.pos - point).norm() <= (disc.radius):
                    rbg_under_disc = screen.get_at((int(x),int(y)))[:3]
                    
    def reset(self, disc):
        disc.pos = self.tee.pos
    def draw(self):
        self.fairway.draw()
        self.tee.draw()
        for tree in self.trees:
            tree.draw()
        self.basket.draw()

class Course:
    def __init__(self, holes):
        self.current_hole = 1
        self.holes = holes
    def hole(self):
        return self.holes[self.current_hole - 1]
    def next_hole(self):
        self.current_hole = self.current_hole + 1
        return self.current_hole <= len(self.holes)
    def draw(self):
        screen.fill(color.GREEN)
        self.holes[self.current_hole - 1].draw()

fairway1 = Fairway(Vec2(340, 100), 120, 400)
tee1 = Tee(Vec2(390, 480))
trees1 = [Circle(Vec2(450, 300), 5, color.DARK_GREEN),
          Circle(Vec2(400, 350), 5, color.DARK_GREEN),
          Circle(Vec2(350, 300), 5, color.DARK_GREEN)]
basket1 = Circle(Vec2(400, 120), 10, color.GREY)
hole1 = Hole(fairway1, tee1, trees1, basket1)

fairway2 = Fairway(Vec2(340, 100), 120, 400)
tee2 = Tee(Vec2(390, 480))
trees2 = [Circle(Vec2(440, 200), 5, color.DARK_GREEN),
          Circle(Vec2(420, 250), 5, color.DARK_GREEN),
          Circle(Vec2(400, 300), 5, color.DARK_GREEN),
          Circle(Vec2(380, 350), 5, color.DARK_GREEN),
          Circle(Vec2(360, 400), 5, color.DARK_GREEN)]
basket2 = Circle(Vec2(400, 120), 10, color.GREY)
hole2 = Hole(fairway2, tee2, trees2, basket2)

fairway3 = Fairway(Vec2(340, 100), 120, 400)
tee3 = Tee(Vec2(390, 480))
trees3 = [Circle(Vec2(440, 200), 5, color.DARK_GREEN),
          Circle(Vec2(420, 250), 5, color.DARK_GREEN),
          Circle(Vec2(400, 300), 5, color.DARK_GREEN),
          Circle(Vec2(380, 250), 5, color.DARK_GREEN),
          Circle(Vec2(360, 200), 5, color.DARK_GREEN)]
basket3 = Circle(Vec2(400, 120), 10, color.GREY)
hole3 = Hole(fairway3, tee3, trees3, basket3)

COURSE = Course([hole1, hole2, hole3])
