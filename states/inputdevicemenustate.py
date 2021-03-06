import statemachine
from states.mainmenustate import MainMenuState, MenuItem, color_normal, color_hover
from settings import Settings
from helpers import load_font, draw_text, load_sound


class InputDeviceMenuState(MainMenuState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_parmas):
        # Get needed settings
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']

        # Save enter parameters
        self.num_players = enter_parmas['num_players']

        # Load fonts
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)
        load_font('fonts\\font.ttf', 'large', self.cached_fonts, 64)

        # Load sounds
        load_sound('sounds\\enter_menu_item.wav',
                   'enter_menu_item', self.cached_sounds)

        self.menu_items = {
            'mouse': MenuItem((self.window_width * 2 // 5, self.window_height * 5 // 8), '>> Mouse', self.cached_fonts['medium']),
            'keyboard': MenuItem((self.window_width * 2 // 5, self.window_height * 6 // 8), '>> Keyboard', self.cached_fonts['medium']),
            'back': MenuItem((self.window_width // 20, self.window_height * 14 // 15), '< Back', self.cached_fonts['medium'])
        }

    def render(self, render_screen):
        draw_text(render_screen, self.cached_fonts['large'], color_normal, True, "Please select your preferred", (
            self.window_width // 2, self.window_height // 8))
        draw_text(render_screen, self.cached_fonts['large'], color_normal, True, "input device", (
            self.window_width // 2, self.window_height // 4))
        for _, value in self.menu_items.items():
            value.render(render_screen)

    def menu_item_callback(self, name):
        if name == 'back':
            statemachine.StateMachine.instance().pop()
        else:
            statemachine.StateMachine.instance().push('difficulty_menu', {
                'num_players': self.num_players,
                'input_device': name
            })
