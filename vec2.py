import math

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @classmethod
    def from_tuple(cls, tuple):
        return cls(tuple[0], tuple[1])
    def as_tuple(self):
        return [self.x, self.y]
    def __add__(self, rhs):
        return Vec2(self.x + rhs.x, self.y + rhs.y)
    def __sub__(self, rhs):
        return Vec2(self.x - rhs.x, self.y - rhs.y)
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)
    def norm(self):
        return math.sqrt(self.norm2())
    def norm2(self):
        return pow(self.x, 2) + pow(self.y, 2)