import statemachine
from states.mainmenustate import MainMenuState, MenuItem, color_normal, color_hover
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from helpers import load_font, draw_text, load_sound


class InputDeviceMenuState(MainMenuState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_parmas):
        self.num_players = enter_parmas['num_players']

        # Load fonts
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)
        load_font('fonts\\font.ttf', 'large', self.cached_fonts, 64)

        # Load sounds
        load_sound('sounds\\enter_menu_item.wav',
                   'enter_menu_item', self.cached_sounds)

        self.menu_items = {
            'mouse': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 5 // 8), '>> Mouse', self.cached_fonts['medium']),
            'keyboard': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 6 // 8), '>> Keyboard', self.cached_fonts['medium']),
        }

    def render(self, render_screen):
        draw_text(render_screen, self.cached_fonts['large'], color_normal, True, "Please select your preferred", (
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8))
        draw_text(render_screen, self.cached_fonts['large'], color_normal, True, "input device", (
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        for _, value in self.menu_items.items():
            value.render(render_screen)

    def menu_item_callback(self, name):
        statemachine.StateMachine.instance().set_change('difficulty_menu', {
            'num_players': self.num_players,
            'input_device': name
        })
