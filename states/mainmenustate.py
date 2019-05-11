import pygame
import statemachine
from states.basestate import BaseState
from helpers import load_font, draw_text, play_music, load_sound
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

color_normal = (255, 255, 255)
color_hover = (255, 255, 0)


class MenuItem():
    def __init__(self, position, text, font):
        self.position = position
        self.text = text
        self.font = font
        self.color = color_normal

    def contains_point(self, point_pos):
        text_render = self.font.render(self.text, True, self.color)
        width = text_render.get_width()
        height = text_render.get_height()

        if point_pos[0] < self.position[0] or point_pos[0] > self.position[0] + width:
            return False
        if point_pos[1] < self.position[1] - height // 2 or point_pos[1] > self.position[1] + height // 2:
            return False

        return True

    def is_mouse_on(self):
        return self.color == color_hover

    def render(self, render_screen):
        draw_text(render_screen, self.font, self.color,
                  True, self.text, self.position, 'left')


class MainMenuState(BaseState):
    def __init__(self):
        super().__init__()
        self.menu_items = {}

    def enter(self, enter_params=None):
        # Load fonts
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)
        load_font('fonts\\font.ttf', 'title', self.cached_fonts, 256)

        # Load sounds
        load_sound('sounds\\enter_menu_item.wav',
                   'enter_menu_item', self.cached_sounds)
        # Play music
        play_music(0, self.music)

        self.menu_items = {
            '1_player': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 4 // 8), '>> 1 Player', self.cached_fonts['medium']),
            '2_players': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 5 // 8), '>> 2 Players', self.cached_fonts['medium']),
            'demo': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 6 // 8), '>> Demo', self.cached_fonts['medium']),
            'exit': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 7 // 8), '>> Exit', self.cached_fonts['medium'])
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_click()

    def update(self, dt):
        self.on_mouse_move()

    def render(self, render_screen):
        draw_text(render_screen, self.cached_fonts['title'], color_normal, True, "PONG", (
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        for _, value in self.menu_items.items():
            value.render(render_screen)

    def on_mouse_move(self):
        mouse_pos = pygame.mouse.get_pos()
        for _, value in self.menu_items.items():
            if value.contains_point(mouse_pos):
                if not value.is_mouse_on():
                    self.cached_sounds['enter_menu_item'].play()
                value.color = color_hover
            else:
                value.color = color_normal

    def on_mouse_click(self):
        if not pygame.mouse.get_pressed()[0]:
            return

        for key, value in self.menu_items.items():
            if value.is_mouse_on():
                self.menu_item_callback(key)

    def menu_item_callback(self, name):
        if name == '1_player':
            statemachine.StateMachine.instance().set_change('input_device_menu', {
                'num_players': 1
            })
        elif name == '2_players':
            statemachine.StateMachine.instance().set_change('new_game', {
                'num_players': 2,
                'input_device': 'keyboard'
            })
        elif name == 'demo':
            statemachine.StateMachine.instance().set_change('play', {
                'is_demo': True
            })
        elif name == 'exit':
            statemachine.StateMachine.instance().exit()
        else:
            print('unknown')
