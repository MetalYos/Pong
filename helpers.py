import pygame
import os


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


def load_font(path, name, fonts, size):
    font = fonts.get(name)
    if font is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        font = pygame.font.Font(canonicalized_path, size)
        fonts[name] = font


def load_sound(path, name, sounds):
    sound = sounds.get(name)
    if sound is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        sounds[name] = sound


def play_music(index, music_list):
    if index < 0 or index >= len(music_list):
        return

    canonicalized_path = music_list[index].replace(
        '/', os.sep).replace('\\', os.sep)
    pygame.mixer.music.load(canonicalized_path)
    pygame.mixer.music.play(-1)


def draw_text(render_screen, font, color, antialias, text, position, align='center'):
    text_render = font.render(text, antialias, color)
    pos = (position[0] - text_render.get_width() // 2,
           position[1] - text_render.get_height() // 2)
    if align is 'left':
        pos = (position[0], position[1] - text_render.get_height() // 2)
    if align is 'right':
        pos = (position[0] - text_render.get_width(),
               position[1] - text_render.get_height() // 2)

    render_screen.blit(text_render, pos)
