#!/usr/local/bin/python3

import sys
import pygame

import color

from screen import screen
from constants import *
from circle import Circle
from disc import Disc
from wind import Wind
from bag import BAG
from vec2 import Vec2

def DrawHole():
    screen.fill(color.GREEN)
    pygame.draw.ellipse(screen, color.LIGHT_GREEN, [340, 100, 120, 400])
    pygame.draw.rect(screen, color.LIGHT_GREY, [390, 480, 20, 50])

pygame.init()

clock = pygame.time.Clock()

mouse_down = False
stroke_count = 0

basket = Circle(Vec2(400, 120), 10, color.GREY)
trees = [Circle(Vec2(400, 300), 5, color.DARK_GREEN), Circle(Vec2(400, 350), 5, color.DARK_GREEN), Circle(Vec2(350, 300), 5, color.DARK_GREEN)]
wind = Wind(Vec2(100, 100), 50, max_speed=50)
disc = Disc(Vec2(400, 500), 5, color=BAG[0].color, resistance_coef=BAG[0].resistance_coef)
validSpace = True

while True:
    # Track Mouse Position at all Times
    mouse = Vec2.from_tuple(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change disc parameters
            for slot in BAG:
                if slot.hit(mouse) and disc.speed() == 0.0:
                    disc.color = slot.color
                    disc.resistance_coef = slot.resistance_coef
            # Space not valid when choosing discs
        for slot in BAG:
            if slot.hit(mouse):
                validSpace = False
                break
        if event.type == pygame.QUIT:
            sys.exit()
        if validSpace == True:
            if event.type == pygame.MOUSEBUTTONDOWN and disc.speed() == 0:
                mouse_down = True
                pygame.mouse.get_rel()
                click_start = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and mouse_down:
                mouse_down = False
                disc.throw(pygame.mouse.get_rel())
                stroke_count = stroke_count + 1
        validSpace = True

    # Update disc
    if not disc.hit(basket):
        disc.update_velocity(FRAME_PERIOD, wind)
        if disc.speed() < 15:
            disc.stop()
        disc.update_position(FRAME_PERIOD)
    else:
        print("Completed the hole in", stroke_count, "strokes.")
        break

    if disc.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
        print("Disc exited the play area.")
        break

    # Detect obstacle collisions
    for tree in trees:
        if disc.hit(tree):
            disc.vel = Vec2(0.0, 0.0)

    # Draw objects
    DrawHole()
    basket.draw()
    wind.draw()

    for tree in trees:
        tree.draw()
    if mouse_down:
        pygame.draw.line(screen, color.YELLOW, click_start, pygame.mouse.get_pos(), width=5)

    # Change color of bag slot if hovering over an option
    for slot in BAG:
        slot.draw(hoverCheck=slot.hit(mouse))

    disc.draw()

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
