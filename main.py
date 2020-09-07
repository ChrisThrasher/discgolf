#!/usr/local/bin/python3

import sys
import numpy as np
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

def DrawBag(discSlot, hoverCheck):
    if hoverCheck == True:
        pygame.draw.circle(screen,
                           color.LIGHT_GREY,
                           [int(discSlot.pos.x + 0.5 * discSlot.r), int(discSlot.pos.y + 0.5 * discSlot.r)],
                           int((discSlot.r + 10) * 0.5),
                           width=0)
    discSlot.draw(discSlot.color)
    textSurface = pygame.font.Font('freesansbold.ttf', 12).render(discSlot.name, True, color.WHITE)
    textRect = textSurface.get_rect()
    textRect.center = (int(discSlot.pos.x + discSlot.r * 0.5), int(discSlot.pos.y - 15))
    screen.blit(textSurface, textRect)

pygame.init()

clock = pygame.time.Clock()

mouse_down = False
stroke_count = 0

basket = Circle(Vec2(390, 120), 20)
trees = [Circle(Vec2(400, 300), 10), Circle(Vec2(400, 350), 10), Circle(Vec2(350, 300), 10)]
wind = Wind(50, 50, 100, max_speed=50)
disc = Disc(Vec2(395, 500), 10, color=BAG[0].color, resistance_coef=BAG[0].resistance_coef)
validSpace = True

while True:
    # Track Mouse Position at all Times
    mouse = Vec2.from_tuple(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change Disc Logic
            for discs in BAG:
                if (discs.center - mouse).norm() <= discs.r and disc.speed() == 0.0:
                    disc.color = discs.color
                    disc.resistance_coef = discs.resistance_coef
            # Space Not Valid when Choosing Discs
        for discs in BAG:
            if (discs.center - mouse).norm() <= discs.r:
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
    basket.draw(color.GREY)
    disc.draw()
    wind.draw()

    for tree in trees:
        tree.draw(color.DARK_GREEN)
    if mouse_down:
        pygame.draw.line(screen, color.YELLOW, click_start, pygame.mouse.get_pos(), width=5)

    # Change Color of Bag Display if Hovering over an Option
    for discs in BAG:
        if (discs.center - mouse).norm() <= discs.r:
            DrawBag(discs, hoverCheck=True)
        else:
            DrawBag(discs, hoverCheck=False)

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
