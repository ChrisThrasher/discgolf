#!/usr/local/bin/python3

import numpy as np
import pygame

from Circle import Circle
from Disc import Disc

pygame.init()
running = True;

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
frame_rate = 60;
frame_period = 1.0 / frame_rate;

def DrawCircle(circle, color):
    pygame.draw.ellipse(screen, color, [int(circle.x), int(circle.y), circle.radius, circle.radius])

class Tree(Circle):
    def draw(self):
        DrawCircle(self, (11, 61, 17))

class Basket(Circle):
    def draw(self):
        DrawCircle(self, (82, 82, 82))

class Hole():
    def draw(self):
        COLOR_ROUGH = (16, 122, 39)
        COLOR_FAIRWAY = (16, 163, 48)
        COLOR_TEE = (155, 155, 155)

        screen.fill(COLOR_ROUGH)
        pygame.draw.ellipse(screen, COLOR_FAIRWAY, [340, 100, 120, 400])
        pygame.draw.rect(screen, COLOR_TEE, [390, 480, 20, 50])

class Wind(Circle):
    def __init__(self, x, y, radius, max_speed):
        super().__init__(x, y, radius)
        self.speed   = np.random.rand() * max_speed
        self.heading = np.deg2rad(np.random.randint(360))
        self.vx = self.speed * np.cos(self.heading)
        self.vy = self.speed * np.sin(self.heading)
    def draw(self):
        DrawCircle(self,(201, 191, 189))
        needleColor = (255, 255, 255)
        start_pos = (int(self.x + self.radius * 0.5),
                     int(self.y + self.radius * 0.5))
        end_pos = (int(start_pos[0] + 0.5 * self.radius * np.cos(self.heading)),
                   int(start_pos[1] + 0.5 * self.radius * np.sin(self.heading)))
        width = 5
        pygame.draw.line(screen, needleColor, start_pos, end_pos, width)
        self.message_display(('Wind Speed: ' + str(round(self.speed,1))))
    def text_objects(self,text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()
    def message_display(self,text):
        windSpeedText = pygame.font.Font('freesansbold.ttf',16)
        TextSurf, TextRect = self.text_objects(text, windSpeedText)
        TextRect.center = (int(self.x + self.radius * 0.5), int(self.y - 15))
        screen.blit(TextSurf, TextRect)
    vx: float = 0.0
    vy: float = 0.0
    speed: float = 0.0
    heading: float = 0.0

hole = Hole()
disc = Disc(395, 500, 10)
basket = Basket(390, 120, 20)
mouse_down = False
mouse_pos = pygame.mouse.get_pos()
stroke_count = 0

trees = [Tree(400, 300, 10), Tree(400, 350, 10), Tree(350, 300, 10)]
wind = Wind(50, 50, 100, max_speed=50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if(pygame.mouse.get_pressed()[0] and mouse_down == False and disc.speed() == 0):
        mouse_down = True
        pygame.mouse.get_rel()
        mouse_pos = pygame.mouse.get_pos()
    elif(not pygame.mouse.get_pressed()[0] and mouse_down == True):
        mouse_down = False
        mouse_movement = pygame.mouse.get_rel()
        disc.vx = mouse_movement[0] * 2 + wind.vx
        disc.vy = mouse_movement[1] * 2 + wind.vy
        stroke_count = stroke_count + 1

    if (not disc.hit(basket)):
        disc.update_velocity(frame_period, wind)
        if(disc.speed() < 15):
            disc.stop()
        disc.update_position(frame_period)
    else:
        print("Completed the hole in", stroke_count, "strokes.")
        running = False

    if (disc.off_screen(screen_width, screen_height)):
        print("Disc exited the play area.")
        running = False

    # Obstacle Check
    for tree in trees:
        if (disc.hit(tree)):
            disc.vx = 0
            disc.vy = 0

    hole.draw()
    basket.draw()
    DrawCircle(disc, (176, 23, 12))
    wind.draw()
    for tree in trees:
        tree.draw()
    if(mouse_down):
        pygame.draw.line(screen, (227, 220, 32), mouse_pos, pygame.mouse.get_pos(), width=5)

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
