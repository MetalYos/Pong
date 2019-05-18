import pygame
import statemachine
from states.mainmenustate import MainMenuState, MenuItem
from helpers import load_font, draw_text, play_music, load_sound
from settings import Settings


class NewGameState(MainMenuState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_params=None):
        # Get needed settings
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']
        self.win_score = Settings.instance().settings['win_score']

        # Save enter parameters
        self.num_players = enter_params['num_players']
        self.input_device = enter_params['input_device']
        self.difficulty = enter_params.get('difficulty')

        # Load font
        load_font('fonts\\font.ttf', 'small_medium', self.cached_fonts, 32)
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)
        load_sound('sounds\\enter_menu_item.wav',
                   'enter_menu_item', self.cached_sounds)

        self.menu_items = {
            'back': MenuItem((self.window_width // 20, self.window_height * 14 // 15), '< Back', self.cached_fonts['medium'])
        }

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    statemachine.StateMachine.instance().set_change('play', {
                        'num_players': self.num_players,
                        'input_device': self.input_device,
                        'difficulty': self.difficulty
                    })

    def render(self, render_screen):
        start_pos = self.window_height // 5
        gap = 40

        if self.num_players == 1:
            draw_text(render_screen, self.cached_fonts['medium'], (255, 255, 255),
                      True, "Player 1 instructions", (self.window_width // 2, start_pos))
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, f"You have chosen to use the {self.input_device}. ", (self.window_width // 2, start_pos))
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, f"You have selected {self.difficulty} difficulty. ", (self.window_width // 2, start_pos))

            if self.input_device == 'mouse':
                start_pos += gap * 2
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, "Control the paddle on the left hand side of the screen", (self.window_width // 8, start_pos), 'left')
                start_pos += gap
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, "using your mouse. the paddle can be moved up or down.", (self.window_width // 8, start_pos), 'left')

            if self.input_device == 'keyboard':
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, "Control the paddle on the left hand side of the screen", (self.window_width // 8, start_pos), 'left')
                start_pos += gap
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, 'using your keyboard. use "W" to move the paddle up', (self.window_width // 8, start_pos), 'left')
                start_pos += gap
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, 'and "S" to move the paddle down.', (self.window_width // 8, start_pos), 'left')
        else:
            draw_text(render_screen, self.cached_fonts['medium'], (255, 255, 255),
                      True, "Two players instructions", (self.window_width // 2, start_pos))
            start_pos += gap * 2
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, 'Player 1 controls the left hand paddle using the', (self.window_width // 8, start_pos), 'left')
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, '"W" (up) and "Z" (down) keys.', (self.window_width // 8, start_pos), 'left')
            start_pos += gap * 2
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, 'Player 2 controls the right hand paddle using the', (self.window_width // 8, start_pos), 'left')
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, 'up arrow and down arrow keys.', (self.window_width // 8, start_pos), 'left')

        start_pos += gap * 2
        draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                  True, "Points are scored when your opponent misses the ball.", (self.window_width // 8, start_pos), 'left')
        start_pos += gap
        draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                  True, f"First player to reach {self.win_score} points wins the game.", (self.window_width // 8, start_pos), 'left')

        start_pos = self.window_height - gap * 2
        draw_text(render_screen, self.cached_fonts['medium'], (255, 255, 255),
                  True, "Press Spacebar to Play!", (self.window_width // 2, start_pos))

        for _, value in self.menu_items.items():
            value.render(render_screen)

    def menu_item_callback(self, name):
        if name == 'back':
            statemachine.StateMachine.instance().pop()
