#!/usr/local/bin/python3

import sys
import pygame

import color

from screen import screen, FRAME_RATE, SCREEN_WIDTH, SCREEN_HEIGHT
from disc import Disc
from bag import BAG
from vec2 import Vec2
from mouse import Mouse
from course import COURSE

pygame.init()

# Mutable global state
clock = pygame.time.Clock()
mouse = Mouse()
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
                COURSE.hole().throw()

    # Update disc
    if not disc.hit(COURSE.hole().basket):
        disc.update_velocity(COURSE.wind)
        if disc.speed() < 15:
            disc.stop()
        disc.update_position()
    else:
        if COURSE.next_hole():
            disc.pos = COURSE.hole().tee.center()
            disc.stop()
        else:
            break

    if disc.off_screen():
        print("Disc exited the play area.")
        break

    # Detect obstacle collisions
    COURSE.hole().check_collision(disc)

    # Draw objects
    COURSE.draw()
    BAG.draw(mouse)
    disc.draw()
    mouse.draw()

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

def button(msg, x, y, w, h, ic, ac, action):
    if x + w > mouse.get_pos().x > x and y + h > mouse.get_pos().y > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if pygame.mouse.get_pressed()[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    font = pygame.font.SysFont(None, 48)
    text_surf = font.render(msg, True, color.WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w // 2)), (y + (h // 2)))
    screen.blit(text_surf, text_rect)

while True:
    pygame.event.clear()
    screen.fill(color.BLACK)
    button('Click to Exit', SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, color.BLACK, color.LIGHT_GREY, sys.exit)
    pygame.display.update()