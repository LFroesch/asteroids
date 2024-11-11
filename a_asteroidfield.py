import pygame
import random
from a_asteroid import Asteroid
from az_constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, asteroids, updatable, drawable):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_timer = 0.0
        self.asteroids = pygame.sprite.Group()
        self.updatable = updatable
        self.drawable = drawable

    def spawn(self, radius, position, velocity):
        #print(f"Spawning asteroid: radius={radius}, position={position}, velocity={velocity}") #FULL DEBUG
        #print(f"Spawning Asteroid!") #GUI Friendly #Hashed out for clarity
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        self.asteroids.add(asteroid)
        self.updatable.add(asteroid)
        self.drawable.add(asteroid)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def add_asteroids(self, new_asteroids):
        for asteroid in new_asteroids:
            self.asteroids.add(asteroid)  # Assuming you're using a sprite group