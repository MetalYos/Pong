import pygame
import statemachine
from states.basestate import BaseState
from helpers import load_font, draw_text, play_music
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WIN_SCORE


class NewGameState(BaseState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_params=None):
        self.num_players = enter_params['num_players']
        self.input_device = enter_params['input_device']
        self.difficulty = enter_params.get('difficulty')

        # Load font
        load_font('fonts\\font.ttf', 'small_medium', self.cached_fonts, 32)
        load_font('fonts\\font.ttf', 'medium', self.cached_fonts, 48)

        # Play music
        play_music(0, self.music)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    statemachine.StateMachine.instance().set_change('play', {
                        'num_players': self.num_players,
                        'input_device': self.input_device,
                        'difficulty': self.difficulty
                    })

    def render(self, render_screen):
        start_pos = WINDOW_HEIGHT // 5
        gap = 40

        if self.num_players == 1:
            draw_text(render_screen, self.cached_fonts['medium'], (255, 255, 255),
                      True, "Player 1 instructions", (WINDOW_WIDTH // 2, start_pos))
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, f"You have chosen to use the {self.input_device}. ", (WINDOW_WIDTH // 2, start_pos))
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, f"You have selected {self.difficulty} difficulty. ", (WINDOW_WIDTH // 2, start_pos))

            if self.input_device == 'mouse':
                start_pos += gap * 2
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, "Control the paddle on the left hand side of the screen", (WINDOW_WIDTH // 8, start_pos), 'left')
                start_pos += gap
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, "using your mouse. the paddle can be moved up or down.", (WINDOW_WIDTH // 8, start_pos), 'left')

            if self.input_device == 'keyboard':
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, "Control the paddle on the left hand side of the screen", (WINDOW_WIDTH // 8, start_pos), 'left')
                start_pos += gap
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, 'using your keyboard. use "W" to move the paddle up', (WINDOW_WIDTH // 8, start_pos), 'left')
                start_pos += gap
                draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                          True, 'and "S" to move the paddle down.', (WINDOW_WIDTH // 8, start_pos), 'left')
        else:
            draw_text(render_screen, self.cached_fonts['medium'], (255, 255, 255),
                      True, "Two players instructions", (WINDOW_WIDTH // 2, start_pos))
            start_pos += gap * 2
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, 'Player 1 controls the left hand paddle using the', (WINDOW_WIDTH // 8, start_pos), 'left')
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, '"W" (up) and "Z" (down) keys.', (WINDOW_WIDTH // 8, start_pos), 'left')
            start_pos += gap * 2
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, 'Player 2 controls the right hand paddle using the', (WINDOW_WIDTH // 8, start_pos), 'left')
            start_pos += gap
            draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                      True, 'up arrow and down arrow keys.', (WINDOW_WIDTH // 8, start_pos), 'left')

        start_pos += gap * 2
        draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                  True, "Points are scored when your opponent misses the ball.", (WINDOW_WIDTH // 8, start_pos), 'left')
        start_pos += gap
        draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255),
                  True, f"First player to reach {WIN_SCORE} points wins the game.", (WINDOW_WIDTH // 8, start_pos), 'left')

        start_pos = WINDOW_HEIGHT - gap * 2
        draw_text(render_screen, self.cached_fonts['medium'], (255, 255, 255),
                  True, "Press Spacebar to Play!", (WINDOW_WIDTH // 2, start_pos))
