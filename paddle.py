import pygame
import random
from settings import Settings
from powermeter import PowerMeter
import math


class Paddle():
    def __init__(self, x, y, width, height):
        self.x = x - width // 2
        self.y = y - height // 2
        self.width = width
        self.height = height
        self.score = 0
        self.load_settings()

        self.speed = self.paddle_speed
        self.tolerance = 0

        self.power_meter = PowerMeter(0, 0, self.x < self.window_width // 2)
        self.power_meter.y = self.window_height - \
            self.power_meter.height - self.window_height // 20
        self.power_meter.x = self.window_width // 2 - \
            self.power_meter.width - self.window_width // 20
        if self.x > self.window_width // 2:
            self.power_meter.x = self.window_width // 2 + self.window_width // 20

        self.reset_ball_hits()

    def load_settings(self):
        # Get needed settings
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']
        self.paddle_speed = Settings.instance().settings['paddle_speed']
        self.paddle_special_hit_threshold = Settings.instance(
        ).settings['paddle_special_hit_threshold']

    def set_position(self, x, y):
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    def get_position(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    def add_ball_hit(self):
        self.ball_hits += 1
        self.power_meter.percentage = 100 * \
            (self.ball_hits / self.paddle_special_hit_threshold)

    def reset_ball_hits(self):
        self.ball_hits = 0
        self.power_meter.percentage = 0
        self.going_to_hit_special = False
        self.hit_special = False

    def move(self, move_up, dt):
        if move_up:
            self.y = max(0, self.y - self.speed * dt)
        else:
            self.y = min(self.window_height - self.height,
                         self.y + self.speed * dt)

    def update(self, dt, ball):
        speed = ball.get_position()[1] - self.get_position()[1]
        x_speed = self.tolerance + (1 - abs(ball.get_position()
                                            [0] - self.get_position()[0]) / self.window_width)
        self.y = self.y + speed * dt * int(x_speed)

    def demo(self, ball):
        self.set_position(self.get_position()[0], ball.get_position()[1])
        if self.y < 0:
            self.y = 0
        if self.y > self.window_height - self.height:
            self.y = self.window_height - self.height

    def draw(self, screen):
        # draw power meter
        self.power_meter.render(screen)

        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(self.x, self.y,
                                     self.width, self.height))
