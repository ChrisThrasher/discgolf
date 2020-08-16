#!/usr/local/bin/python3

import math
import pygame

pygame.init()

COLOR_ROUGH = (16, 122, 39)
COLOR_FAIRWAY = (16, 163, 48)
COLOR_TEE = (155, 155, 155)
COLOR_HOLE = (82, 82, 82)
COLOR_DISC = (176, 23, 12)

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
frame_rate = 60;
frame_period = 1.0 / frame_rate;

class Vec2:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init
    x: float
    y: float

disc = Vec2(395, 500)
disc_velocity = Vec2(0, -40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if (math.sqrt(pow(disc.x - 400, 2) + pow(disc.y - 130, 2)) > 10):
        disc.x = frame_period * disc_velocity.x + disc.x
        disc.y = frame_period * disc_velocity.y + disc.y

    screen.fill(COLOR_ROUGH)

    pygame.draw.ellipse(screen, COLOR_FAIRWAY, [340, 100, 120, 400])
    pygame.draw.rect(screen, COLOR_TEE, [390, 480, 20, 50])
    pygame.draw.ellipse(screen, COLOR_HOLE, [390, 120, 20, 20])
    pygame.draw.ellipse(screen, COLOR_DISC, [disc.x, disc.y, 10, 10])

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
