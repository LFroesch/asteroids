from circleshape import CircleShape
from constants import *
import pygame
import math
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (radius, radius), radius, 2)
        self.rect = self.image.get_rect(center = (x, y))
	
    def draw(self, screen):
        surface.blit(self.image, self.rect)
    
    def update(self, dt):
         self.position += self.velocity * dt
         self.rect.center = self.position
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        new_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_velocity1 = self.velocity.rotate(new_angle) * 1.2
        new_velocity2 = self.velocity.rotate(-new_angle) * 1.2
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = new_velocity1
        new_asteroid2.velocity = new_velocity2
        #print("-      Created new asteroids at:        -")
        #print(f"- {new_asteroid1.position}+{new_asteroid2.position} -") Hashed out for clean GUI
        new_asteroids = (new_asteroid1, new_asteroid2)
        return new_asteroids
        