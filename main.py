#!/usr/local/bin/python3

import sys
import numpy as np
import pygame

import Color

from Constants import *
from Circle import Circle
from Disc import Disc
from Wind import Wind

def DrawCircle(circle, color):
    pygame.draw.ellipse(screen, color, [int(circle.x), int(circle.y), circle.radius, circle.radius])

def DrawWind(wind):
    DrawCircle(wind, Color.LIGHT_GREY)
    start_pos = (int(wind.x + wind.radius * 0.5),
                 int(wind.y + wind.radius * 0.5))
    end_pos = (int(start_pos[0] + 0.5 * wind.radius * np.cos(wind.heading)),
               int(start_pos[1] + 0.5 * wind.radius * np.sin(wind.heading)))
    width = 5
    pygame.draw.line(screen, Color.BLACK, start_pos, end_pos, width)
    wind_speed_text = pygame.font.Font('freesansbold.ttf', 16)
    text = ('Wind Speed: ' + str(round(wind.speed, 1)))
    text_surf, text_rect = wind.text_objects(text, wind_speed_text)
    text_rect.center = (int(wind.x + wind.radius * 0.5), int(wind.y - 15))
    screen.blit(text_surf, text_rect)

def DrawHole():
    screen.fill(Color.GREEN)
    pygame.draw.ellipse(screen, Color.LIGHT_GREEN, [340, 100, 120, 400])
    pygame.draw.rect(screen, Color.LIGHT_GREY, [390, 480, 20, 50])

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

mouse_down = False
mouse_pos = pygame.mouse.get_pos()
stroke_count = 0

disc = Disc(395, 500, 10)
basket = Circle(390, 120, 20)
trees = [Circle(400, 300, 10), Circle(400, 350, 10), Circle(350, 300, 10)]
wind = Wind(50, 50, 100, max_speed=50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and disc.speed() == 0:
            mouse_down = True
            pygame.mouse.get_rel()
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and mouse_down:
            mouse_down = False
            disc.throw(pygame.mouse.get_rel())
            stroke_count = stroke_count + 1

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
            disc.vx = 0
            disc.vy = 0

    # Draw objects
    DrawHole()
    DrawCircle(basket, Color.GREY)
    DrawCircle(disc, Color.RED)
    DrawWind(wind)
    for tree in trees:
        DrawCircle(tree, Color.DARK_GREEN)
    if mouse_down:
        pygame.draw.line(screen, Color.YELLOW, mouse_pos, pygame.mouse.get_pos(), width=5)

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
