import statemachine
from states.mainmenustate import MainMenuState, MenuItem, color_normal, color_hover
from settings import Settings
from helpers import load_font, draw_text, load_sound


class GameMenuState(MainMenuState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_params=None):
        # Get needed settings
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']

        # Load fonts
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)
        load_font('fonts\\font.ttf', 'title', self.cached_fonts, 256)

        # Load sounds
        load_sound('sounds\\enter_menu_item.wav',
                   'enter_menu_item', self.cached_sounds)

        self.menu_items = {
            'resume': MenuItem((self.window_width // 3, self.window_height * 5 // 8), '>> Resume Game', self.cached_fonts['medium']),
            'new_game': MenuItem((self.window_width // 3, self.window_height * 6 // 8), '>> New Game', self.cached_fonts['medium']),
            'exit': MenuItem((self.window_width // 3, self.window_height * 7 // 8), '>> Exit', self.cached_fonts['medium'])
        }

    def render(self, render_screen):
        draw_text(render_screen, self.cached_fonts['title'], color_normal, True, "PONG", (
            self.window_width // 2, self.window_height // 4))
        for _, value in self.menu_items.items():
            value.render(render_screen)

    def menu_item_callback(self, name):
        if name == 'resume':
            statemachine.StateMachine.instance().pop()
        elif name == 'new_game':
            statemachine.StateMachine.instance().set_change('main_menu')
        elif name == 'exit':
            statemachine.StateMachine.instance().exit()
        else:
            print('unknown')
