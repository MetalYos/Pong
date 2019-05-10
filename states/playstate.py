import pygame
import random
import statemachine
from constants import *
from states.basestate import BaseState
from helpers import load_sound, load_font, draw_text, play_music
from paddle import Paddle
from ball import Ball


class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.serving_player = 1
        self.winner = 1

    def enter(self, enter_params=None):
        self.num_players = enter_params['num_players']
        self.input_device = enter_params['input_device']
        self.difficulty = enter_params['difficulty']

        # Load Fonts
        load_font('fonts\\font.ttf', 'huge', self.cached_fonts, 128)

        # Load Sounds
        load_sound('sounds\\paddle_hit.wav', 'paddle_hit', self.cached_sounds)
        load_sound('sounds\\score.wav', 'score', self.cached_sounds)
        load_sound('sounds\\wall_hit.wav', 'wall_hit', self.cached_sounds)

        # Play music
        play_music(1, self.music)

        # Create Entites
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BALL_RADIUS)
        self.player1 = Paddle(
            PADDLE_WIDTH // 2, PADDLE_HEIGHT // 2 + 100, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.player2 = Paddle(WINDOW_WIDTH - PADDLE_WIDTH // 2, WINDOW_HEIGHT -
                              PADDLE_HEIGHT // 2 - 100, PADDLE_WIDTH, PADDLE_HEIGHT)

        self.ball.set_initial_speed(self.serving_player == 2)

        # Set tolerance according to difficulty
        tolerance = random.randint(
            PADDLE_TOLERANCE_BEGINNER[0], PADDLE_TOLERANCE_BEGINNER[1]) / 100
        self.speed_increase = PADDLE_SPEED_INCREASE_BEGINNER
        if self.difficulty == 'intermediate':
            tolerance = random.randint(
                PADDLE_TOLERANCE_INTERMEDIATE[0], PADDLE_TOLERANCE_INTERMEDIATE[1]) / 100
            self.speed_increase = PADDLE_SPEED_INCREASE_INTERMEDIATE
        if self.difficulty == 'expert':
            tolerance = random.randint(
                PADDLE_TOLERANCE_EXPERT[0], PADDLE_TOLERANCE_EXPERT[1]) / 100
            self.speed_increase = PADDLE_SPEED_INCREASE_EXPERT
        self.player2.set_tolerance(tolerance)

    def exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    statemachine.StateMachine.instance().push('game_menu')

    def update(self, dt):
        if self.input_device == 'keyboard':
            self.on_keypress(dt)
        else:
            self.on_mouse_move()

        self.ball.update(dt)

        if self.num_players == 1:
            self.player2.update(dt, self.ball)

        # Ball collision with upper bound
        if self.ball.top() <= 0:
            self.ball.dy = -self.ball.dy
            self.ball.set_position(self.ball.get_position()[
                0], self.ball.radius)
            self.cached_sounds['wall_hit'].play()

        # Ball collision with lower bound
        if self.ball.bottom() > WINDOW_HEIGHT:
            self.ball.dy = -self.ball.dy
            self.ball.set_position(self.ball.get_position()[
                0], WINDOW_HEIGHT - self.ball.radius)
            self.cached_sounds['wall_hit'].play()

        # Ball collision with player1
        if self.ball.collides(self.player1):
            self.ball.set_position(
                self.player1.width + self.ball.radius + 1, self.ball.get_position()[1])
            self.ball.dx = -self.ball.dx * 1.03

            if self.ball.get_position()[1] < self.player1.get_position()[1]:
                self.ball.dy = -(random.randint(BALL_INITIAL_MIN_SPEED, BALL_INITIAL_MAX_SPEED)
                                 * self.player1.get_position()[1]) / self.ball.get_position()[1]
            else:
                self.ball.dy = (random.randint(BALL_INITIAL_MIN_SPEED, BALL_INITIAL_MAX_SPEED)
                                * (self.player1.get_position()[1] + self.player1.height // 2)) / self.ball.get_position()[1]
            self.cached_sounds['paddle_hit'].play()

        # Ball collision with player2
        if self.ball.collides(self.player2):
            self.ball.set_position(
                WINDOW_WIDTH - self.player2.width - self.ball.radius - 1, self.ball.get_position()[1])
            self.ball.dx = -self.ball.dx * 1.03

            if self.ball.get_position()[1] - self.ball.radius < self.player2.get_position()[1]:
                self.ball.dy = -(random.randint(BALL_INITIAL_MIN_SPEED, BALL_INITIAL_MAX_SPEED)
                                 * self.player2.get_position()[1]) / self.ball.get_position()[1]
            else:
                self.ball.dy = (random.randint(BALL_INITIAL_MIN_SPEED, BALL_INITIAL_MAX_SPEED)
                                * (self.player2.get_position()[1] + self.player2.height // 2)) / self.ball.get_position()[1]
            self.cached_sounds['paddle_hit'].play()

        # Player 1 scores
        if self.ball.left() > WINDOW_WIDTH:
            self.player1.score += 1
            self.serving_player = 2
            self.cached_sounds['score'].play()
            if self.player1.score == WIN_SCORE:
                self.winner = 1
                statemachine.StateMachine.instance().set_change('win', {
                    'winner': self.winner,
                    'player1_score': self.player1.score,
                    'player2_score': self.player2.score
                })
            else:
                self.ball.reset()
                self.ball.set_initial_speed(self.serving_player == 2)
                pygame.time.wait(500)

        # Player 2 scores
        if self.ball.right() < 0:
            self.player2.score += 1
            self.serving_player = 1
            self.cached_sounds['score'].play()
            if self.player2.score == WIN_SCORE:
                self.winner = 2
                statemachine.StateMachine.instance().set_change('win', {
                    'winner': self.winner,
                    'player1_score': self.player1.score,
                    'player2_score': self.player2.score
                })
            else:
                self.ball.reset()
                self.ball.set_initial_speed(self.serving_player == 2)
                pygame.time.wait(500)

    def render(self, render_screen):
        # draw the net
        self.draw_net(render_screen)

        # draw the score
        draw_text(render_screen, self.cached_fonts['huge'], (255, 255, 255), True, str(
            self.player1.score), (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
        draw_text(render_screen, self.cached_fonts['huge'], (255, 255, 255), True, str(
            self.player2.score), (WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT // 4))

        # Draw the ball
        self.ball.draw(render_screen)
        # Draw the paddles
        self.player1.draw(render_screen)
        self.player2.draw(render_screen)

    def draw_net(self, render_screen):
        start_pos = (WINDOW_WIDTH // 2, 0)
        end_pos = (start_pos[0], start_pos[1] + NET_SEGMENT_HEIGHT)
        pygame.draw.line(render_screen, (255, 255, 255),
                         start_pos, end_pos, NET_SEGMENT_WIDTH)

        for _ in range(1, NET_SEGMENTS):
            start_pos = (end_pos[0], end_pos[1] + NET_SEGMENTS_GAP)
            end_pos = (start_pos[0], start_pos[1] + NET_SEGMENT_HEIGHT)
            pygame.draw.line(render_screen, (255, 255, 255),
                             start_pos, end_pos, NET_SEGMENT_WIDTH)

    def on_keypress(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.player1.move(True, dt)
        elif pressed[pygame.K_s]:
            self.player1.move(False, dt)

        if self.num_players == 2:
            if pressed[pygame.K_UP]:
                self.player2.move(True, dt)
            elif pressed[pygame.K_DOWN]:
                self.player2.move(False, dt)

    def on_mouse_move(self):
        position = pygame.mouse.get_pos()
        self.player1.set_position(self.player1.get_position()[0], position[1])
