import pygame
import random
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, PADDLE_SPEED, PADDLE_SPECIAL_HIT_THRESHOLD
from powermeter import PowerMeter
import math


class Paddle():
    def __init__(self, x, y, width, height):
        self.x = x - width // 2
        self.y = y - height // 2
        self.width = width
        self.height = height
        self.score = 0
        self.ball_hits = 0
        self.going_to_hit_special = False
        self.hit_special = False

        self.speed = PADDLE_SPEED
        self.tolerance = 0

        self.power_meter = PowerMeter(0, 0, self.x < WINDOW_WIDTH // 2)
        self.power_meter.y = WINDOW_HEIGHT - self.power_meter.height - WINDOW_HEIGHT // 20
        self.power_meter.x = WINDOW_WIDTH // 2 - \
            self.power_meter.width - WINDOW_WIDTH // 20
        if self.x > WINDOW_WIDTH // 2:
            self.power_meter.x = WINDOW_WIDTH // 2 + WINDOW_WIDTH // 20

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
            (self.ball_hits / PADDLE_SPECIAL_HIT_THRESHOLD)

    def reset_ball_hits(self):
        self.ball_hits = 0
        self.power_meter.percentage = 0

    def move(self, move_up, dt):
        if move_up:
            self.y = max(0, self.y - self.speed * dt)
        else:
            self.y = min(WINDOW_HEIGHT - self.height, self.y + self.speed * dt)

    def update(self, dt, ball):
        speed = ball.get_position()[1] - self.get_position()[1]
        x_speed = self.tolerance + (1 - abs(ball.get_position()
                                            [0] - self.get_position()[0]) / WINDOW_WIDTH)
        self.y = self.y + speed * dt * int(x_speed)

    def demo(self, ball):
        self.set_position(self.get_position()[0], ball.get_position()[1])
        if self.y < 0:
            self.y = 0
        if self.y > WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height

    def draw(self, screen):
        # draw power meter
        self.power_meter.render(screen)

        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(self.x, self.y,
                                     self.width, self.height))
