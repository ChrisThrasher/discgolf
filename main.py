#!/usr/local/bin/python3

import math
import numpy as np
import pygame

pygame.init()
running = True;

COLOR_ROUGH = (16, 122, 39)
COLOR_FAIRWAY = (16, 163, 48)
COLOR_TEE = (155, 155, 155)
COLOR_ARROW = (227, 220, 32)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
frame_rate = 60;
frame_period = 1.0 / frame_rate;

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self, color):
        pygame.draw.ellipse(screen, color, [int(self.x), int(self.y), self.radius, self.radius])
    x: int
    y: int
    radius: int

class Disc(Circle):
    def update_position(self):
        self.x = frame_period * self.vx + self.x
        self.y = frame_period * self.vy + self.y
    def update_velocity(self):
        wind_resistance = 0.0004
        self.vx = self.vx - np.sign(self.vx) * wind_resistance * pow(self.vx, 2)
        self.vy = self.vy - np.sign(self.vy) * wind_resistance * pow(self.vy, 2)
    def hit(self, obs):
        if(pow(obs.x - self.x, 2) + pow(obs.y - self.y, 2) <= pow((self.radius + obs.radius) / 2, 2)):
            return True
        return False
    def speed(self):
        return math.sqrt(pow(self.vx, 2) + pow(self.vy, 2))
    def stop(self):
        self.vx = 0
        self.vy = 0
    def draw(self):
        Circle.draw(self, (176, 23, 12))
    vx: int = 0
    vy: int = 0

class Tree(Circle):
    def draw(self):
        Circle.draw(self, (11, 61, 17))

class Hole(Circle):
    def draw(self):
        Circle.draw(self, (82, 82, 82))

disc = Disc(395, 500, 10)
hole = Hole(390, 120, 20)
mouse_down = False
mouse_pos = pygame.mouse.get_pos()
stroke_count = 0

trees = [Tree(400, 300, 10), Tree(400, 350, 10), Tree(350, 300, 10)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if(pygame.mouse.get_pressed()[0] and mouse_down == False and disc.vx == 0 and disc.vy == 0):
        mouse_down = True
        pygame.mouse.get_rel()
        mouse_pos = pygame.mouse.get_pos()
    elif(not pygame.mouse.get_pressed()[0] and mouse_down == True):
        mouse_down = False
        mouse_movement = pygame.mouse.get_rel()
        disc.vx = mouse_movement[0] * 2
        disc.vy = mouse_movement[1] * 2
        stroke_count = stroke_count + 1

    if (not disc.hit(hole)):
        disc.update_velocity()
        if(disc.speed() < 30):
            disc.stop()
        disc.update_position()
    else:
        print("Completed the hole in", stroke_count, "strokes.")
        running = False

    if (disc.x < 0 or disc.x > screen_width or disc.y < 0 or disc.y > screen_height):
        print("Exited the play area.")
        running = False

    # Obstacle Check
    for tree in trees:
        if (disc.hit(tree)):
            disc.vx = 0
            disc.vy = 0

    screen.fill(COLOR_ROUGH)

    pygame.draw.ellipse(screen, COLOR_FAIRWAY, [340, 100, 120, 400])
    pygame.draw.rect(screen, COLOR_TEE, [390, 480, 20, 50])
    hole.draw()
    disc.draw()
    for tree in trees:
        tree.draw()
    if(mouse_down):
        pygame.draw.line(screen, COLOR_ARROW, mouse_pos, pygame.mouse.get_pos(), width=5)

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
