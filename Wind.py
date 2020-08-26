import numpy as np

from Circle import Circle

class Wind(Circle):
    def __init__(self, x, y, radius, max_speed):
        super().__init__(x, y, radius)
        self.speed   = np.random.rand() * max_speed
        self.heading = np.deg2rad(np.random.randint(360))
        self.vx = self.speed * np.cos(self.heading)
        self.vy = self.speed * np.sin(self.heading)
    def text_objects(self,text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()
    vx: float = 0.0
    vy: float = 0.0
    speed: float = 0.0
    heading: float = 0.0
