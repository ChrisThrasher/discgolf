import pygame
import os
import color

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
    def check_collision(self, disc):
        for tree in self.trees:
            if disc.hit(tree):
                tree_to_disc = disc.pos - tree.pos
                direction = tree_to_disc / tree_to_disc.norm()
                disc.pos = direction * (tree.radius + disc.radius + 5) + tree.pos
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

class Course:
    def __init__(self, holes):
        self.current_hole = 0
        self.holes = holes
    def hole(self):
        return self.holes[self.current_hole]
    def next_hole(self):
        print(f"Completed hole {self.current_hole + 1} in {self.hole().stroke_count} strokes.")
        self.current_hole += 1
        return self.current_hole < len(self.holes)
    def draw(self):
        self.holes[self.current_hole].draw()

hole1 = Hole("Hole1.png", Tee(Vec2(390, 480)), Basket(Vec2(440, 160)), [Tree(Vec2(450, 110)),
                                                                        Tree(Vec2(400, 100)),
                                                                        Tree(Vec2(350, 120)),
                                                                        Tree(Vec2(490, 140)),
                                                                        Tree(Vec2(455, 210)),
                                                                        Tree(Vec2(400, 350))])

hole2 = Hole("Hole2.png", Tee(Vec2(390, 480)), Basket(Vec2(225, 120)), [Tree(Vec2(265, 200)),
                                                                        Tree(Vec2(255, 240)),
                                                                        Tree(Vec2(310, 265)),
                                                                        Tree(Vec2(310, 335))])

hole3 = Hole("Hole3.png", Tee(Vec2(280, 480)), Basket(Vec2(530, 140)), [Tree(Vec2(450, 190)),
                                                                        Tree(Vec2(385, 300)),
                                                                        Tree(Vec2(390, 230)),
                                                                        Tree(Vec2(355, 425)),
                                                                        Tree(Vec2(350, 470)),
                                                                        Tree(Vec2(350, 385))])

COURSE = Course([hole1, hole2, hole3])
