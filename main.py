#!/usr/local/bin/python3

import math
import numpy as np
import pygame

pygame.init()
running = True;

COLOR_ROUGH = (16, 122, 39)
COLOR_FAIRWAY = (16, 163, 48)
COLOR_TEE = (155, 155, 155)
COLOR_HOLE = (82, 82, 82)
COLOR_DISC = (176, 23, 12)
COLOR_ARROW = (227, 220, 32)
COLOR_TREE = (11, 61, 17)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
frame_rate = 60;
frame_period = 1.0 / frame_rate;

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    x: int
    y: int

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
    def hit(self, obs):
        if(pow(obs.x - self.x, 2) + pow(obs.y - self.y, 2) <= pow((self.radius + obs.radius) / 2, 2)):
            return True
        return False
    def stop(self):
        self.vx = 0
        self.vy = 0
    vx: int = 0
    vy: int = 0

disc = Disc(395, 500, 10)
hole = Circle(390, 120, 20)
mouse_down = False
mouse_pos = pygame.mouse.get_pos()
stroke_count = 0

trees = [Circle(400, 300, 10), Circle(400, 350, 10), Circle(350, 300, 10)]

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
        disc.vx = mouse_movement[0]
        disc.vy = mouse_movement[1]
        stroke_count = stroke_count + 1

    if (not disc.hit(hole)):
        wind_resistance = 0.0004
        disc.vx = disc.vx - np.sign(disc.vx) * wind_resistance * pow(disc.vx, 2)
        disc.vy = disc.vy - np.sign(disc.vy) * wind_resistance * pow(disc.vy, 2)
        cutoff_velocity = 30
        if(math.sqrt(pow(disc.vx, 2) + pow(disc.vy, 2)) < cutoff_velocity):
            disc.stop()
        disc.x = frame_period * disc.vx + disc.x
        disc.y = frame_period * disc.vy + disc.y
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
    hole.draw(COLOR_HOLE)
    disc.draw(COLOR_DISC)
    for tree in trees:
        tree.draw(COLOR_TREE)
    if(mouse_down):
        pygame.draw.line(screen, COLOR_ARROW, mouse_pos, pygame.mouse.get_pos(), width=5)

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
