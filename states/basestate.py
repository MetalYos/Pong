import pygame
import os


class BaseState():
    def __init__(self):
        self.cached_fonts = {}
        self.cached_sounds = {}
        self.music = ['music\\short_night.mp3', 'music\\revo_nation.mp3']

    def enter(self, enter_params=None):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def handle_events(self, events):
        pass

    def render(self, render_screen):
        pass
