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
from course import COURSE

pygame.init()
clock = pygame.time.Clock()
stroke_count = 0
mouse = Mouse()

wind = Wind(Vec2(100, 100), 50, max_speed=50)
disc = Disc(COURSE.hole().tee.center(), 5, color=BAG[0].color, resistance_coef=BAG[0].resistance_coef)

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
    if not disc.hit(COURSE.hole().basket):
        disc.update_velocity(wind)
        if disc.speed() < 15:
            disc.stop()
        disc.update_position()
    else:
        print("Completed the hole in", stroke_count, "strokes.")
        if COURSE.next_hole():
            disc.pos = COURSE.hole().tee.center()
            disc.stop()
            stroke_count = 0
        else:
            break

    if disc.off_screen():
        print("Disc exited the play area.")
        break

    # Detect obstacle collisions
    if COURSE.hole().check_collision(disc):
        disc.stop()

    # Draw objects
    COURSE.draw()
    wind.draw()

    # Change color of bag slot if hovering over an option
    for slot in BAG:
        slot.draw(hover_check=mouse.overlaps(slot))

    disc.draw()
    mouse.draw()

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
