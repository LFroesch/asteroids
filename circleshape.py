from constants import *
import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
    
    def check_collision(self, other_shape):
        return self.position.distance_to(other_shape.position) < self.radius + other_shape.radius
    
    def off_screen(self):
        return (self.position.x < 0 or self.position.x > SCREEN_WIDTH
                 or self.position.y < 0 or self.position.y > SCREEN_HEIGHT)