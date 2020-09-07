import math

from circle import Circle
from vec2 import Vec2

class Disc(Circle):
    def __init__(self, pos, radius, color, resistance_coef):
        super().__init__(pos, radius)
        self.vel = Vec2(0.0, 0.0)
        self.color = color
        self.resistance_coef = resistance_coef
        self.height = 1.0
    def update_position(self, dt):
        self.pos = self.vel * dt + self.pos
    def update_velocity(self, dt, wind):
        if (self.height < 0 or self.speed() == 0):
            self.stop()
            return
        self.height = self.height - 0.005
        resistive_accel = self.resistance_coef * self.relative_speed2(wind)
        self.vel.x = self.vel.x - resistive_accel * math.cos(self.relative_heading(wind)) * dt
        self.vel.y = self.vel.y - resistive_accel * math.sin(self.relative_heading(wind)) * dt
    def throw(self, mouse_movement):
        self.vel = Vec2(mouse_movement[0], mouse_movement[1]) * 2.0
    def hit(self, obs):
        return (self.pos - obs.pos).norm2() <= pow((self.radius + obs.radius) / 2, 2)
    def speed(self):
        return self.vel.norm()
    def relative_speed2(self, wind):
        return (self.vel - wind.vel).norm2()
    def relative_heading(self, wind):
        relative_speed = self.vel - wind.vel
        return math.atan2(relative_speed.y, relative_speed.x)
    def off_screen(self, width, height):
        return self.pos.x < 0 or self.pos.x > width or self.pos.y < 0 or self.pos.y > height
    def stop(self):
        self.vel = Vec2(0.0, 0.0)
        self.height = 1.0
