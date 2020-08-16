#!/usr/local/bin/python3

import math
import pygame

pygame.init()

COLOR_ROUGH = (16, 122, 39)
COLOR_FAIRWAY = (16, 163, 48)
COLOR_TEE = (155, 155, 155)
COLOR_HOLE = (82, 82, 82)
COLOR_DISC = (176, 23, 12)
COLOR_ARROW = (232, 78, 35)

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
frame_rate = 60;
frame_period = 1.0 / frame_rate;

class Vec2:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init
    x: int
    y: int

disc = Vec2(395, 500)
disc_velocity = Vec2(0, 0)
mouse_down = False
mouse_pos = pygame.mouse.get_pos()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if(pygame.mouse.get_pressed()[0] and mouse_down == False):
        mouse_down = True
        pygame.mouse.get_rel()
        mouse_pos = pygame.mouse.get_pos()
    elif(not pygame.mouse.get_pressed()[0] and mouse_down == True):
        mouse_down = False
        mouse_movement = pygame.mouse.get_rel()
        disc_velocity.x = mouse_movement[0]
        disc_velocity.y = mouse_movement[1]

    if (math.sqrt(pow(disc.x - 400, 2) + pow(disc.y - 130, 2)) > 10):
        disc.x = frame_period * disc_velocity.x + disc.x
        disc.y = frame_period * disc_velocity.y + disc.y

    screen.fill(COLOR_ROUGH)

    pygame.draw.ellipse(screen, COLOR_FAIRWAY, [340, 100, 120, 400])
    pygame.draw.rect(screen, COLOR_TEE, [390, 480, 20, 50])
    pygame.draw.ellipse(screen, COLOR_HOLE, [390, 120, 20, 20])
    pygame.draw.ellipse(screen, COLOR_DISC, [disc.x, disc.y, 10, 10])
    if(mouse_down):
        pygame.draw.line(screen, COLOR_ARROW, mouse_pos, pygame.mouse.get_pos(), width=5)

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
