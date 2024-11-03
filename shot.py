from circleshape import CircleShape
from constants import SHOT_RADIUS, SHOT_RADIUS2, SHOT_RADIUS3, PLAYER_SHOOT_SPEED
import pygame
import math


class Shot(CircleShape):
	def __init__(self, x, y, rotation):
		super().__init__(x, y, SHOT_RADIUS)
		self.velocity = pygame.Vector2(0, -1).rotate(rotation) * PLAYER_SHOOT_SPEED
		self.position = pygame.math.Vector2(x, y)
		self.image = pygame.Surface((SHOT_RADIUS*2, SHOT_RADIUS*2), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (255, 255, 255), (SHOT_RADIUS, SHOT_RADIUS), SHOT_RADIUS)
		self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
	
	def update(self, dt):
		self.position += self.velocity * dt
		self.rect.center = (self.position.x, self.position.y)
		if self.off_screen():
			self.kill()

class Shot2(CircleShape):
	def __init__(self, x, y, rotation):
		super().__init__(x, y, SHOT_RADIUS2)
		self.velocity = pygame.Vector2(0, -1).rotate(rotation) * PLAYER_SHOOT_SPEED
		self.position = pygame.math.Vector2(x, y)
		self.image = pygame.Surface((SHOT_RADIUS2*2, SHOT_RADIUS2*2), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (255, 255, 255), (SHOT_RADIUS2, SHOT_RADIUS2), SHOT_RADIUS2)
		self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
	
	def update(self, dt):
		self.position += self.velocity * dt
		self.rect.center = (self.position.x, self.position.y)
		if self.off_screen():
			self.kill()

class Shot3(CircleShape):
	def __init__(self, x, y, rotation):
		super().__init__(x, y, SHOT_RADIUS3)
		self.velocity = pygame.Vector2(0, -1).rotate(rotation) * PLAYER_SHOOT_SPEED
		self.position = pygame.math.Vector2(x, y)
		self.image = pygame.Surface((SHOT_RADIUS3*2, SHOT_RADIUS3*2), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (255, 255, 255), (SHOT_RADIUS3, SHOT_RADIUS3), SHOT_RADIUS3)
		self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
	
	def update(self, dt):
		self.position += self.velocity * dt
		self.rect.center = (self.position.x, self.position.y)
		if self.off_screen():
			self.kill()