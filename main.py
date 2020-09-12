#!/usr/local/bin/python3

import sys
import pygame

from screen import FRAME_RATE
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
disc = Disc(COURSE.hole().tee.center(), 5, BAG.selected)

while True:
    # Track mouse position at all times
    mouse.pos = Vec2.from_tuple(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and disc.speed() == 0:
            if BAG.is_selected(mouse) and disc.speed() == 0.0:
                disc.change_slot(BAG.selected)
                break
            mouse.down()
            pygame.mouse.get_rel()
        if event.type == pygame.MOUSEBUTTONUP and mouse.clicking:
            mouse.up()
            if mouse.relative_throw_vec.norm() > 0.0:
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
    COURSE.hole().check_collision(disc)

    # Draw objects
    COURSE.draw()
    wind.draw()
    BAG.draw(mouse)
    disc.draw()
    mouse.draw()

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
