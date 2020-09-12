#!/usr/local/bin/python3

import sys
import pygame

import color

from screen import screen, FRAME_RATE
from circle import Circle
from disc import Disc
from wind import Wind
from bag import BAG
from vec2 import Vec2
from mouse import Mouse
from course import *

pygame.init()
clock = pygame.time.Clock()
stroke_count = 0
mouse = Mouse()

basket = Circle(Vec2(400, 120), 10, color.GREY)
trees = [Circle(Vec2(450, 300), 5, color.DARK_GREEN),
         Circle(Vec2(400, 350), 5, color.DARK_GREEN),
         Circle(Vec2(350, 300), 5, color.DARK_GREEN)]
wind = Wind(Vec2(100, 100), 50, max_speed=50)
disc = Disc(Vec2(400, 500), 5, color=BAG[0].color, resistance_coef=BAG[0].resistance_coef)
course = Course()

while True:
    # Track mouse position at all times
    mouse.pos = Vec2.from_tuple(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and disc.speed() == 0:
            for slot in BAG:
                if mouse.overlaps(slot) and disc.speed() == 0.0:
                    disc.color = slot.color
                    disc.resistance_coef = slot.resistance_coef
                    break
            mouse.down()
            pygame.mouse.get_rel()
        if event.type == pygame.MOUSEBUTTONUP and mouse.clicking:
            mouse.up()
            disc.throw(mouse.relative_throw_vec)
            stroke_count = stroke_count + 1

    # Update disc
    if not disc.hit(basket):
        disc.update_velocity(wind)
        if disc.speed() < 15:
            disc.stop()
        disc.update_position()
    else:
        print("Completed the hole in", stroke_count, "strokes.")
        if not course.next_hole():
            break

    if disc.off_screen():
        print("Disc exited the play area.")
        break

    # Detect obstacle collisions
    for tree in trees:
        if disc.hit(tree):
            disc.vel = Vec2(0.0, 0.0)

    # Draw objects
    course.draw()
    basket.draw()
    wind.draw()

    for tree in trees:
        tree.draw()

    # Change color of bag slot if hovering over an option
    for slot in BAG:
        slot.draw(hover_check=mouse.overlaps(slot))

    disc.draw()
    mouse.draw()

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
