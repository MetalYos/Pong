import pygame
import os
from settings import Settings


class PowerMeter():
    def __init__(self, x, y, is_left):
        self.x = x
        self.y = y
        self.is_left = is_left
        if is_left:
            self.img_border = pygame.image.load(
                os.path.join('images', 'power_meter_border_left.png'))
            self.img_inner = pygame.image.load(
                os.path.join('images', 'power_meter_inner_left.png'))
        else:
            self.img_border = pygame.image.load(
                os.path.join('images', 'power_meter_border_right.png'))
            self.img_inner = pygame.image.load(
                os.path.join('images', 'power_meter_inner_right.png'))
        self.percentage = 0
        self.width = Settings.instance().settings['window_width'] // 6
        self.height = Settings.instance().settings['window_height'] // 12

        self.img_inner = pygame.transform.scale(
            self.img_inner, (self.width - 5, self.height - 5))
        self.img_border = pygame.transform.scale(
            self.img_border, (self.width, self.height))

    def render(self, render_screen):
        x_width = int((self.percentage / 100.0) * self.width)
        if not self.is_left:
            area = pygame.Rect(self.width - x_width, 0, x_width, self.height)
            render_screen.blit(
                self.img_inner, (self.x + self.width - x_width, self.y), area)
        else:
            area = pygame.Rect(0, 0, x_width, self.height)
            render_screen.blit(self.img_inner, (self.x, self.y), area)

        render_screen.blit(self.img_border, (self.x, self.y))
