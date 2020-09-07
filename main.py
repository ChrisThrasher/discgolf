#!/usr/local/bin/python3

import sys
import numpy as np
import pygame

import color

from constants import *
from circle import Circle
from disc import Disc
from wind import Wind
from discBag import BagSlot

def DrawCircle(circle, color):
    pygame.draw.ellipse(screen, color, [int(circle.x), int(circle.y), circle.radius, circle.radius])

def DrawWind(wind):
    DrawCircle(wind, color.LIGHT_GREY)
    start_pos = (int(wind.x + wind.radius * 0.5),
                 int(wind.y + wind.radius * 0.5))
    end_pos = (int(start_pos[0] + 0.5 * wind.radius * np.cos(wind.heading)),
               int(start_pos[1] + 0.5 * wind.radius * np.sin(wind.heading)))
    pygame.draw.line(screen, color.WHITE, start_pos, end_pos, width=5)
    wind_speed_text = pygame.font.Font('freesansbold.ttf', 16)
    text = ('Wind Speed: ' + str(round(wind.speed, 1)))
    text_surf, text_rect = wind.text_objects(text, wind_speed_text)
    text_rect.center = (int(wind.x + wind.radius * 0.5), int(wind.y - 15))
    screen.blit(text_surf, text_rect)

def DrawHole():
    screen.fill(color.GREEN)
    pygame.draw.ellipse(screen, color.LIGHT_GREEN, [340, 100, 120, 400])
    pygame.draw.rect(screen, color.LIGHT_GREY, [390, 480, 20, 50])

def DrawBag(discSlot, hoverCheck):
    if hoverCheck == True:
        pygame.draw.circle(screen,
                           color.LIGHT_GREY,
                           [int(discSlot.x + 0.5 * discSlot.r), int(discSlot.y + 0.5 * discSlot.r)],
                           int((discSlot.r + 10) * 0.5),
                           width=0)
    DrawCircle(discSlot, discSlot.color)
    discTypeText = pygame.font.Font('freesansbold.ttf', 12)
    TextSurf, TextRect = discSlot.text_objects(discSlot.discType, discTypeText)
    TextRect.center = (int(discSlot.x + discSlot.r * 0.5), int(discSlot.y - 15))
    screen.blit(TextSurf, TextRect)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

mouse_down = False
mouse_pos = pygame.mouse.get_pos()
stroke_count = 0

basket = Circle(390, 120, 20)
trees = [Circle(400, 300, 10), Circle(400, 350, 10), Circle(350, 300, 10)]
wind = Wind(50, 50, 100, max_speed=50)
bag = [BagSlot(750, 50, 40, color.WHITE, discType='Driver'),
       BagSlot(700, 50, 40, color.BLUE, discType='Mid Range'),
       BagSlot(650, 50, 40, color.ORANGE, discType='Putter')]
disc = Disc(395, 500, 10, color=bag[0].color, resistance_coef=bag[0].resistance_coef)
validSpace = True

while True:
    # Track Mouse Position at all Times
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change Disc Logic
            for discs in bag:
                if pow(discs.xc - mouse[0], 2) + pow(discs.yc - mouse[1], 2) <= pow(discs.r, 2):
                    disc.color = discs.color
                    disc.resistance_coef = discs.resistance_coef
            # Space Not Valid when Choosing Discs
        for discs in bag:
            if pow(discs.xc - mouse[0], 2) + pow(discs.yc - mouse[1], 2) <= pow(discs.r, 2):
                validSpace = False
                break
        if event.type == pygame.QUIT:
            sys.exit()
        if validSpace == True:
            if event.type == pygame.MOUSEBUTTONDOWN and disc.speed() == 0:
                mouse_down = True
                pygame.mouse.get_rel()
                mouse_pos = pygame.mouse.get_pos()
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
            disc.vx = 0
            disc.vy = 0

    # Draw objects
    DrawHole()
    DrawCircle(basket, color.GREY)
    DrawCircle(disc, disc.color)
    DrawWind(wind)

    # Change Color of Bag Display if Hovering over an Option
    for discs in bag:
        if pow(discs.xc - mouse[0], 2) + pow(discs.yc - mouse[1], 2) <= pow(discs.r, 2):
            DrawBag(discs, hoverCheck=True)
        else:
            DrawBag(discs, hoverCheck=False)

    for tree in trees:
        DrawCircle(tree, color.DARK_GREEN)
    if mouse_down:
        pygame.draw.line(screen, color.YELLOW, mouse_pos, pygame.mouse.get_pos(), width=5)

    # Finish cycle
    pygame.display.update()
    clock.tick(FRAME_RATE)

pygame.quit()
