import statemachine
from states.mainmenustate import MainMenuState, MenuItem, color_normal, color_hover
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from helpers import load_font, draw_text, load_sound


class DifficultyMenuState(MainMenuState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_parmas):
        self.num_players = enter_parmas['num_players']
        self.input_device = enter_parmas['input_device']

        # Load fonts
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)
        load_font('fonts\\font.ttf', 'large', self.cached_fonts, 64)

        # Load sounds
        load_sound('sounds\\enter_menu_item.wav',
                   'enter_menu_item', self.cached_sounds)

        self.menu_items = {
            'beginner': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 3 // 8), '>> Beginner', self.cached_fonts['medium']),
            'intermediate': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 4 // 8), '>> Intermediate', self.cached_fonts['medium']),
            'expert': MenuItem((WINDOW_WIDTH * 2 // 5, WINDOW_HEIGHT * 5 // 8), '>> Expert', self.cached_fonts['medium'])
        }

    def render(self, render_screen):
        draw_text(render_screen, self.cached_fonts['large'], color_normal, True, "Choose your difficulty level:", (
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8))
        for _, value in self.menu_items.items():
            value.render(render_screen)

    def menu_item_callback(self, name):
        statemachine.StateMachine.instance().set_change('new_game', {
            'num_players': self.num_players,
            'input_device': self.input_device,
            'difficulty': name
        })
