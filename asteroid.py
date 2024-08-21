from circleshape import CircleShape
from constants import *
import pygame
import math

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