import math

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __sub__(self, rhs):
        return Vec2(self.x - rhs.x, self.y - rhs.y)
    def norm(self):
        return math.sqrt(self.norm2())
    def norm2(self):
        return pow(self.x, 2) + pow(self.y, 2)
    x: int
    y: int