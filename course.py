import pygame
import os
import color

from circle import Circle
from screen import screen
from vec2 import Vec2

HOLE1 = pygame.image.load(os.path.join("assets", "Hole1.png"))

class Tree(Circle):
    def __init__(self, pos):
        super().__init__(pos, 5, color.DARK_GREEN)
    def draw(self):
        super().draw()

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
    def __init__(self, background, tee, trees, basket):
        self.background = background
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
    def reset(self, disc):
        disc.pos = self.tee.pos
    def draw(self):
        screen.blit(self.background, (0, 0))
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
        self.holes[self.current_hole - 1].draw()

tee1 = Tee(Vec2(390, 480))
trees1 = [Tree(Vec2(450, 300)),
          Tree(Vec2(400, 350)),
          Tree(Vec2(350, 300))]
basket1 = Circle(Vec2(440, 160), 10, color.GREY)
hole1 = Hole(HOLE1, tee1, trees1, basket1)

tee2 = Tee(Vec2(390, 480))
trees2 = [Tree(Vec2(440, 200)),
          Tree(Vec2(420, 250)),
          Tree(Vec2(400, 300)),
          Tree(Vec2(380, 350)),
          Tree(Vec2(360, 400))]
basket2 = Circle(Vec2(440, 160), 10, color.GREY)
hole2 = Hole(HOLE1, tee2, trees2, basket2)

tee3 = Tee(Vec2(390, 480))
trees3 = [Tree(Vec2(440, 200)),
          Tree(Vec2(420, 250)),
          Tree(Vec2(400, 300)),
          Tree(Vec2(380, 250)),
          Tree(Vec2(360, 200))]
basket3 = Circle(Vec2(440, 160), 10, color.GREY)
hole3 = Hole(HOLE1, tee3, trees3, basket3)

COURSE = Course([hole1, hole2, hole3])
