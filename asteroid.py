from circleshape import CircleShape
from constants import *
import pygame
import math
import random

class Asteroid(CircleShape):
    original_image = None
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        if Asteroid.original_image is None:
            Asteroid.original_image = pygame.image.load("asteroid.png").convert_alpha()
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius
        scaled_size = int(radius * 2)
        self.image = pygame.transform.scale(Asteroid.original_image, (scaled_size, scaled_size))
        self.rect = self.image.get_rect(center = (x, y))
        self.rotation_speed = random.uniform(-90, 90)  # degrees per second
        self.angle = 0
        self.original_scaled = self.image
	
    def draw(self, screen):
        #print("Asteroid draw called")
        super().draw(screen)
        screen.blit(self.image, self.rect)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.angle += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.original_scaled, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        new_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_velocity1 = self.velocity.rotate(new_angle) * 1.125
        new_velocity2 = self.velocity.rotate(-new_angle) * 1.125
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = new_velocity1
        new_asteroid2.velocity = new_velocity2
        #print("-      Created new asteroids at:        -")
        #print(f"- {new_asteroid1.position}+{new_asteroid2.position} -") Hashed out for clean GUI
        new_asteroids = (new_asteroid1, new_asteroid2)
        return new_asteroids
        