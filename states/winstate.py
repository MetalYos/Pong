import pygame
import statemachine
from states.basestate import BaseState
from helpers import load_font, draw_text
from constants import *


class WinState(BaseState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_params):
        self.winner = enter_params['winner']
        self.player1_score = enter_params['player1_score']
        self.player2_score = enter_params['player2_score']

        # Load fonts
        load_font('fonts\\font.ttf', 'small', self.cached_fonts, 24)
        load_font('fonts\\font.ttf', 'large', self.cached_fonts, 64)
        load_font('fonts\\font.ttf', 'huge', self.cached_fonts, 128)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    statemachine.StateMachine.instance().set_change('main_menu')

    def render(self, render_screen):
        draw_text(render_screen, self.cached_fonts['large'], (255, 255, 255),
                  True, f'Player {self.winner} Won!', (
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
        draw_text(render_screen, self.cached_fonts['small'], (255, 255, 255),
                  True, "Press Enter to go back to the main menu", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))

        # print score
        draw_text(render_screen, self.cached_fonts['huge'], (255, 255, 255), True, str(
            self.player1_score), (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
        draw_text(render_screen, self.cached_fonts['huge'], (255, 255, 255), True, str(
            self.player2_score), (WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT // 4))
