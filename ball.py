import pygame
import random
import math
from settings import Settings


class Ball():
    def __init__(self, x, y, radius):
        self.initX = x - radius
        self.initY = y - radius
        self.radius = radius

        self.reset()

    def set_position(self, x, y):
        self.x = x - self.radius
        self.y = y - self.radius

    def get_position(self):
        return (self.x + self.radius, self.y + self.radius)

    def speed(self):
        return math.sqrt(self.dx ** 2 + self.dy ** 2)

    def left(self):
        return self.x

    def right(self):
        return self.x + self.radius

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.radius

    def collides(self, paddle):
        if self.x > paddle.x + paddle.width or paddle.x > self.x + self.radius * 2:
            return False
        if self.y > paddle.y + paddle.height or paddle.y > self.y + self.radius * 2:
            return False

        return True

    def reset(self):
        self.x = self.initX
        self.y = self.initY
        self.dx = 0
        self.dy = 0

    def set_initial_speed(self, is_left=False):
        # Get needed settings
        self.ball_initial_min_speed = Settings.instance(
        ).settings['ball_initial_min_speed']
        self.ball_initial_max_speed = Settings.instance(
        ).settings['ball_initial_max_speed']

        self.dx = random.randint(self.ball_initial_min_speed,
                                 self.ball_initial_max_speed)
        self.dy = random.randint(-self.ball_initial_min_speed,
                                 self.ball_initial_max_speed)

        if is_left:
            self.dx = -self.dx

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(self.x, self.y,
                                     self.radius * 2, self.radius * 2))
