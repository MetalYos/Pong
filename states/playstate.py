import pygame
import random
import math
import statemachine
from settings import Settings
from states.basestate import BaseState
from helpers import load_sound, load_font, draw_text, play_music
from paddle import Paddle
from ball import Ball
from particlesystem import ParticleShape, ParticleSystem
from gradient import Gradient


class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.serving_player = 1
        self.winner = 1
        self.ball_prev_speed = 0

    def enter(self, enter_params=None):
        # Get needed settings
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']
        self.paddle_width = Settings.instance().settings['paddle_width']
        self.paddle_height = Settings.instance().settings['paddle_height']
        self.paddle_tolerance_beginner = Settings.instance(
        ).settings['paddle_tolerance_beginner']
        self.paddle_tolerance_Intermediate = Settings.instance(
        ).settings['paddle_tolerance_Intermediate']
        self.paddle_tolerance_expert = Settings.instance(
        ).settings['paddle_tolerance_expert']
        self.ball_speed_increase_beginner = Settings.instance(
        ).settings['ball_speed_increase_beginner']
        self.ball_speed_increase_intermediate = Settings.instance(
        ).settings['ball_speed_increase_intermediate']
        self.ball_speed_increase_expert = Settings.instance(
        ).settings['ball_speed_increase_expert']
        self.paddle_special_hit_threshold = Settings.instance(
        ).settings['paddle_special_hit_threshold']
        self.paddle_special_hit_increase = Settings.instance(
        ).settings['paddle_special_hit_increase']
        self.net_segments = Settings.instance().settings['net_segments']
        self.net_segments_gap = Settings.instance(
        ).settings['net_segments_gap']
        self.net_segments_height = Settings.instance(
        ).settings['net_segments_height']
        self.net_segment_width = Settings.instance(
        ).settings['net_segment_width']
        self.win_score = Settings.instance().settings['win_score']

        # Save enter parameters
        self.num_players = enter_params.get('num_players')
        self.input_device = enter_params.get('input_device')
        self.difficulty = enter_params.get('difficulty')
        self.is_demo = enter_params.get('is_demo')
        if self.is_demo is None:
            self.is_demo = False

        # Load Fonts
        load_font('fonts\\font.ttf', 'small_medium', self.cached_fonts, 32)
        load_font('fonts\\font.ttf', 'huge', self.cached_fonts, 128)

        # Load Sounds
        load_sound('sounds\\paddle_hit.wav', 'paddle_hit', self.cached_sounds)
        load_sound('sounds\\score.wav', 'score', self.cached_sounds)
        load_sound('sounds\\wall_hit.wav', 'wall_hit', self.cached_sounds)
        load_sound('sounds\\paddle_special_hit.wav',
                   'paddle_special_hit', self.cached_sounds)

        # Play music
        play_music(1, self.music)

        # Create Entites
        self.ball = Ball(self.window_width // 2,
                         self.window_height // 2, Settings.instance().settings['ball_radius'])
        self.player1 = Paddle(
            self.paddle_width // 2, self.paddle_height // 2 + 100, self.paddle_width, self.paddle_height)
        self.player2 = Paddle(self.window_width - self.paddle_width // 2, self.window_height -
                              self.paddle_height // 2 - 100, self.paddle_width, self.paddle_height)

        self.ball.set_initial_speed(self.serving_player == 2)

        # Set tolerance according to difficulty
        tolerance = random.randint(
            self.paddle_tolerance_beginner[0], self.paddle_tolerance_beginner[1]) / 100
        self.speed_increase = self.ball_speed_increase_beginner
        if self.difficulty == 'intermediate':
            tolerance = random.randint(
                self.paddle_tolerance_Intermediate[0], self.paddle_tolerance_Intermediate[1]) / 100
            self.speed_increase = self.ball_speed_increase_intermediate
        if self.difficulty == 'expert':
            tolerance = random.randint(
                self.paddle_tolerance_expert[0], self.paddle_tolerance_expert[1]) / 100
            self.speed_increase = self.ball_speed_increase_expert
        self.player2.set_tolerance(tolerance)

        # Load particle system
        self.particle_system = ParticleSystem(
            self.ball.get_position()[0], self.ball.get_position()[
                1], ParticleShape.SQUARE,
            Settings.instance().settings['particle_size'],
            Settings.instance().settings['particle_birth_rate'],
            Settings.instance().settings['particle_speed'],
            Settings.instance().settings['particle_death_age'])
        gradient = Gradient(Settings.instance().settings['particle_gradient_color_01'],
                            Settings.instance().settings['particle_gradient_last_color'])
        gradient.add_color(Settings.instance().settings['particle_gradient_color_02'],
                           Settings.instance().settings['particle_gradient_color_02_pos'])
        gradient.add_color(Settings.instance().settings['particle_gradient_color_03'],
                           Settings.instance().settings['particle_gradient_color_03_pos'])
        gradient.add_color(Settings.instance().settings['particle_gradient_color_04'],
                           Settings.instance().settings['particle_gradient_color_04_pos'])
        self.particle_system.set_gradient(gradient)
        self.particle_system.set_death_variance(
            Settings.instance().settings['particle_death_variant'])
        self.particle_system.set_speed_variance(
            Settings.instance().settings['particle_speed_variant'])

    def exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.is_demo:
                        statemachine.StateMachine.instance().push('game_menu')
                    else:
                        statemachine.StateMachine.instance().set_change('main_menu')
                if event.key == pygame.K_LCTRL:
                    if self.player1.ball_hits >= self.paddle_special_hit_threshold:
                        self.player1.going_to_hit_special = True
                if event.key == pygame.K_RCTRL:
                    if self.num_players == 2 and self.player2.ball_hits >= self.paddle_special_hit_threshold:
                        self.player2.going_to_hit_special = True

    def update(self, dt):
        if not self.is_demo:
            # Move player/s with keyboard or mouse
            if self.input_device == 'keyboard':
                self.on_keypress(dt)
            else:
                self.on_mouse_move()

            # Update player2 if it is a 1 player game
            if self.num_players == 1:
                self.player2.update(dt, self.ball)
        else:
            self.player1.demo(self.ball)
            self.player2.demo(self.ball)

        # Update ball movement
        self.ball.update(dt)

        # Check collisions with bounds
        self.ball_bounds_collision()

        # Ball collision with player1
        if self.ball.collides(self.player1):
            self.ball_paddle_collision(self.player1)

        # Ball collision with player2
        if self.ball.collides(self.player2):
            self.ball_paddle_collision(self.player2)

        self.particle_system.update(dt)
        self.particle_system.set_position(self.ball.get_position())

        if not self.is_demo:
            # Player 1 scores
            if self.ball.left() > self.window_width:
                self.player_scores(self.player1)

            # Player 2 scores
            if self.ball.right() < 0:
                self.player_scores(self.player2)

    def render(self, render_screen):
        # draw the net
        self.draw_net(render_screen)

        # draw the score
        draw_text(render_screen, self.cached_fonts['huge'], (255, 255, 255), True, str(
            self.player1.score), (self.window_width // 4, self.window_height // 4))
        draw_text(render_screen, self.cached_fonts['huge'], (255, 255, 255), True, str(
            self.player2.score), (self.window_width * 3 // 4, self.window_height // 4))

        # Draw special hit prompt
        time = int(pygame.time.get_ticks() / 500)
        if self.player1.ball_hits == self.paddle_special_hit_threshold:
            if not self.player1.going_to_hit_special:
                if time % 2 == 0:
                    draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255), True,
                              'Press Left Ctrl for a special hit!', (self.window_width * 1 // 4, self.window_height // 10))
            else:
                if time % 2 == 0:
                    draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255), True,
                              'Hitting special!', (self.window_width * 1 // 4, self.window_height // 10))
        if self.num_players == 2 and self.player2.ball_hits == self.paddle_special_hit_threshold:
            if not self.player2.going_to_hit_special:
                if time % 2 == 0:
                    draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255), True,
                              'Press Right Ctrl for a special hit!', (self.window_width * 3 // 4, self.window_height // 10))
            else:
                if time % 2 == 0:
                    draw_text(render_screen, self.cached_fonts['small_medium'], (255, 255, 255), True,
                              'Hitting special!', (self.window_width * 3 // 4, self.window_height // 10))

        # Draw the ball
        self.ball.draw(render_screen)
        # Draw the paddles
        self.player1.draw(render_screen)
        self.player2.draw(render_screen)

        self.particle_system.render(render_screen)

    def draw_net(self, render_screen):
        start_pos = (self.window_width // 2, 0)
        end_pos = (start_pos[0], start_pos[1] + self.net_segments_height)
        pygame.draw.line(render_screen, (255, 255, 255),
                         start_pos, end_pos, self.net_segment_width)

        for _ in range(1, self.net_segments):
            start_pos = (end_pos[0], end_pos[1] + self.net_segments_gap)
            end_pos = (start_pos[0], start_pos[1] + self.net_segments_height)
            pygame.draw.line(render_screen, (255, 255, 255),
                             start_pos, end_pos, self.net_segment_width)

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

    def player_scores(self, player):
        player.score += 1
        self.player1.reset_ball_hits()
        self.player2.reset_ball_hits()

        if player == self.player1:
            self.serving_player = 2
        else:
            self.serving_player = 1
        self.cached_sounds['score'].play()
        if player.score == self.win_score:
            if player == self.player1:
                self.winner = 1
            else:
                self.winner = 2
            statemachine.StateMachine.instance().set_change('win', {
                'winner': self.winner,
                'player1_score': self.player1.score,
                'player2_score': self.player2.score
            })
        else:
            pygame.time.delay(200)
            self.ball.reset()
            self.ball.set_initial_speed(self.serving_player == 2)

    def ball_bounds_collision(self):
        # Ball collision with upper bound
        if self.ball.top() <= 0:
            self.ball.dy = -self.ball.dy
            self.ball.set_position(self.ball.get_position()[
                0], self.ball.radius)
            self.cached_sounds['wall_hit'].play()

        # Ball collision with lower bound
        if self.ball.bottom() > self.window_height:
            self.ball.dy = -self.ball.dy
            self.ball.set_position(self.ball.get_position()[
                0], self.window_height - self.ball.radius)
            self.cached_sounds['wall_hit'].play()

    def ball_paddle_collision(self, player):
        # Add a hit to player
        if player.ball_hits < self.paddle_special_hit_threshold:
            player.add_ball_hit()

        # Set the ball position
        if player == self.player1:
            self.ball.set_position(
                player.width + self.ball.radius + 1, self.ball.get_position()[1])
        else:
            self.ball.set_position(
                self.window_width - player.width - self.ball.radius - 1, self.ball.get_position()[1])

        # Calculate the new speed
        speed = math.sqrt(self.ball.dx ** 2 + self.ball.dy ** 2)
        if self.difficulty == 'beginner':
            speed *= self.ball_speed_increase_beginner
        if self.difficulty == 'intermediate':
            speed *= self.ball_speed_increase_intermediate
        if self.difficulty == 'expert':
            speed *= self.ball_speed_increase_expert
        if player.going_to_hit_special:
            self.ball_prev_speed = self.ball.speed()
            speed *= self.paddle_special_hit_increase
            player.hit_special = True
            player.going_to_hit_special = False
            player.reset_ball_hits()
            self.cached_sounds['paddle_special_hit'].play()

        opponent = self.player1
        if player == self.player1:
            opponent = self.player2
        if opponent.hit_special:
            speed = self.ball_prev_speed
            opponent.hit_special = False

        # Calculate new direction
        direction_y = min(random.random(), 0.6)
        if self.ball.get_position()[1] < player.get_position()[1]:
            direction_y *= -1.0
        direction_x = math.sqrt(1 - direction_y ** 2)
        if player == self.player2:
            direction_x *= -1

        # Calculate the new velocity
        self.ball.dx = direction_x * speed
        self.ball.dy = direction_y * speed

        # Play the paddle hit sound
        self.cached_sounds['paddle_hit'].play()
