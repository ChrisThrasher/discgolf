#!/usr/local/bin/python3

import math
import numpy as np
import pygame

pygame.init()
running = True;

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
frame_rate = 60;
frame_period = 1.0 / frame_rate;

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self, color):
        pygame.draw.ellipse(screen, color, [int(self.x), int(self.y), self.radius, self.radius])
    x: int
    y: int
    radius: int

class Disc(Circle):
    def update_position(self):
        self.x = frame_period * self.vx + self.x
        self.y = frame_period * self.vy + self.y
    def update_velocity(self, wind):
        if (self.height < 0 or self.speed() == 0):
            self.stop()
            return
        self.height = self.height - 0.005
        resistance_coef = 0.015
        resistive_accel = resistance_coef * self.relative_speed2(wind)
        self.vx = self.vx - resistive_accel * math.cos(self.relative_heading(wind)) * frame_period
        self.vy = self.vy - resistive_accel * math.sin(self.relative_heading(wind)) * frame_period
    def hit(self, obs):
        if(pow(obs.x - self.x, 2) + pow(obs.y - self.y, 2) <= pow((self.radius + obs.radius) / 2, 2)):
            return True
        return False
    def speed(self):
        return math.sqrt(pow(self.vx, 2) + pow(self.vy, 2))
    def relative_speed2(self, wind):
        return pow(self.vx - wind.vx, 2) + pow(self.vy - wind.vy, 2)
    def relative_heading(self, wind):
        return math.atan2(self.vy - wind.vy, self.vx - wind.vx)
    def off_screen(self):
        return disc.x < 0 or disc.x > screen_width or disc.y < 0 or disc.y > screen_height
    def stop(self):
        self.vx = 0
        self.vy = 0
        self.height = 1.0
    def draw(self):
        Circle.draw(self, (176, 23, 12))
    vx: float = 0.0
    vy: float = 0.0
    height: float = 1.0

class Tree(Circle):
    def draw(self):
        Circle.draw(self, (11, 61, 17))

class Basket(Circle):
    def draw(self):
        Circle.draw(self, (82, 82, 82))

class Hole():
    def draw(self):
        COLOR_ROUGH = (16, 122, 39)
        COLOR_FAIRWAY = (16, 163, 48)
        COLOR_TEE = (155, 155, 155)

        screen.fill(COLOR_ROUGH)
        pygame.draw.ellipse(screen, COLOR_FAIRWAY, [340, 100, 120, 400])
        pygame.draw.rect(screen, COLOR_TEE, [390, 480, 20, 50])

class Wind(Circle):
    def generateWind(self):
        self.speed   = np.random.rand() * 50.0
        self.heading = np.deg2rad(np.random.randint(360))
        self.vx = self.speed * np.cos(self.heading)
        self.vy = self.speed * np.sin(self.heading)
    def drawCompass(self):
        Circle.draw(self,(201, 191, 189))
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
wind = Wind(50, 50, 100)
wind.generateWind()

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
        disc.update_velocity(wind)
        if(disc.speed() < 15):
            disc.stop()
        disc.update_position()
    else:
        print("Completed the hole in", stroke_count, "strokes.")
        running = False

    if (disc.off_screen()):
        print("Disc exited the play area.")
        running = False

    # Obstacle Check
    for tree in trees:
        if (disc.hit(tree)):
            disc.vx = 0
            disc.vy = 0

    hole.draw()
    basket.draw()
    disc.draw()
    wind.drawCompass()
    for tree in trees:
        tree.draw()
    if(mouse_down):
        pygame.draw.line(screen, (227, 220, 32), mouse_pos, pygame.mouse.get_pos(), width=5)

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
