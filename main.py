#!/usr/local/bin/python3

import pygame

pygame.init()

COLOR_ROUGH = (16, 122, 39)
COLOR_FAIRWAY = (16, 163, 48)
COLOR_TEE = (155, 155, 155)
COLOR_HOLE = (82, 82, 82)

screen = pygame.display.set_mode((800,600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(COLOR_ROUGH)

    pygame.draw.ellipse(screen, COLOR_FAIRWAY, [340,100,120,400])
    pygame.draw.rect(screen, COLOR_TEE, [390, 480, 20, 50])
    pygame.draw.ellipse(screen, COLOR_HOLE, [390, 120, 20, 20])

    pygame.display.update()

pygame.quit()
