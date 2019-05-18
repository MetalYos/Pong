import pygame
import random
import math
from enum import Enum
from gradient import Gradient


class ParticleShape(Enum):
    CIRCLE = 1
    SQUARE = 2


class Particle():
    def __init__(self, shape, size):
        self.shape = shape
        self.size = size
        self.age = 0
        self.velocity = (0, 0)

    def set_position(self, center_x, center_y):
        self.x = center_x
        self.y = center_y

    def set_velocity(self, dx, dy):
        self.velocity = (dx, dy)

    def update(self, dt):
        self.age += 1
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def render(self, render_screen, color):
        if self.shape == ParticleShape.CIRCLE:
            pygame.draw.circle(render_screen, color,
                               (int(self.x), int(self.y)), self.size)
        if self.shape == ParticleShape.SQUARE:
            pygame.draw.rect(render_screen, color,
                             pygame.Rect(self.x - self.size // 2, self.y - self.size // 2,
                                         self.size, self.size))


class ParticleSystem():
    def __init__(self, x, y, shape, size, birth_rate, speed, death_age):
        self.shape = shape
        self.color = None
        self.gradient = None
        self.birth_rate = birth_rate
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.death_age = death_age
        self.death_variance = 0.0
        self.speed_variance = 0.0

        self.particles = []
        self.frame_count = 0

    def set_position(self, pos):
        self.x, self.y = pos

    def set_color(self, color):
        self.color = color
        self.gradient = None

    def set_gradient(self, gradient):
        self.gradient = gradient
        self.color = None

    def set_death_variance(self, variance):
        self.death_variance = variance

    def set_speed_variance(self, variance):
        self.speed_variance = variance

    def birth_particle(self):
        particle = Particle(self.shape, self.size)
        particle.set_position(self.x, self.y)

        # set particle velocity
        dx = random.uniform(-1.0, 1.0)
        dy = random.uniform(-1.0, 1.0)
        length = math.sqrt(dx ** 2 + dy ** 2)
        dx /= length
        dy /= length
        speed = random.uniform(
            1.0 - self.speed_variance, 1.0) * self.speed
        particle.set_velocity(dx * speed, dy * speed)

        self.particles.append(particle)

    def update(self, dt):
        self.frame_count += 1

        # Birth particles according to birth rate
        if self.birth_rate > 1:
            if self.frame_count % self.birth_rate == 0:
                self.birth_particle()
        else:
            num_of_particles = int(1 / self.birth_rate)
            for _ in range(num_of_particles):
                self.birth_particle()

        for particle in self.particles:
            particle.update(dt)

            # Kill particals who are older than death_age
            variant_death_age = random.uniform(
                1.0 - self.death_variance, 1.0) * self.death_age
            if particle.age > variant_death_age:
                self.particles.remove(particle)

    def render(self, render_screen):
        for particle in self.particles:
            if self.color is not None:
                particle.render(render_screen, self.color)
            if self.gradient is not None:
                gradient_pos = particle.age / self.death_age
                color = self.gradient.get_color(gradient_pos)
                particle.render(render_screen, color)
