import math

from circle import Circle

class Disc(Circle):
    def __init__(self, x, y, radius, color, resistance_coef):
        super().__init__(x, y, radius)
        self.color = color
        self.resistance_coef = resistance_coef
    def update_position(self, dt):
        self.x = dt * self.vx + self.x
        self.y = dt * self.vy + self.y
    def update_velocity(self, dt, wind):
        if (self.height < 0 or self.speed() == 0):
            self.stop()
            return
        self.height = self.height - 0.005
        resistance_coef = 0.015
        resistive_accel = resistance_coef * self.relative_speed2(wind)
        self.vx = self.vx - resistive_accel * math.cos(self.relative_heading(wind)) * dt
        self.vy = self.vy - resistive_accel * math.sin(self.relative_heading(wind)) * dt
    def throw(self, mouse_movement):
        throw_gain = 2.0
        self.vx = throw_gain * mouse_movement[0]
        self.vy = throw_gain * mouse_movement[1]
    def hit(self, obs):
        if pow(obs.x - self.x, 2) + pow(obs.y - self.y, 2) <= pow((self.radius + obs.radius) / 2, 2):
            return True
        return False
    def speed(self):
        return math.sqrt(pow(self.vx, 2) + pow(self.vy, 2))
    def relative_speed2(self, wind):
        return pow(self.vx - wind.vx, 2) + pow(self.vy - wind.vy, 2)
    def relative_heading(self, wind):
        return math.atan2(self.vy - wind.vy, self.vx - wind.vx)
    def off_screen(self, width, height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height
    def stop(self):
        self.vx = 0
        self.vy = 0
        self.height = 1.0
    vx: float = 0.0
    vy: float = 0.0
    height: float = 1.0