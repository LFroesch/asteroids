from circleshape import CircleShape
from constants import *
import pygame
import math

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		self.rotation = 0
		self.image = pygame.Surface((PLAYER_RADIUS*2, PLAYER_RADIUS*2), pygame.SRCALPHA)
		self.image.fill((255, 255, 255))  # White color
		self.rect = self.image.get_rect(center=(x, y))
		self.position = pygame.math.Vector2(x, y)
		self.draw_triangle()
	
	def draw_triangle(self):
		self.image.fill((0, 0, 0, 0))
		forward = pygame.Vector2(0, -1).rotate(self.rotation)
		right = forward.rotate(90)
		center = pygame.Vector2(PLAYER_RADIUS, PLAYER_RADIUS)
    
		a = center + forward * PLAYER_RADIUS
		b = center - forward * PLAYER_RADIUS/2 - right * PLAYER_RADIUS/2
		c = center - forward * PLAYER_RADIUS/2 + right * PLAYER_RADIUS/2
    
		pygame.draw.polygon(self.image, "WHITE", [a, b, c])
    
	def update(self, dt):
		self.handle_input(dt)
		self.update_graphics()

	def handle_input(self, dt):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.rotation -= PLAYER_TURN_SPEED * dt
		if keys[pygame.K_d]:
			self.rotation += PLAYER_TURN_SPEED * dt
		if keys[pygame.K_w]:
			self.move(dt)
		if keys[pygame.K_s]:
			self.move(-dt)

	def update_graphics(self):
		self.draw_triangle()
		self.rect.center = self.position

	def move(self, dt):
		direction = pygame.Vector2(math.sin(math.radians(self.rotation)), 
                               -math.cos(math.radians(self.rotation)))
		self.position += direction * PLAYER_SPEED * dt
		#print(f"Rotation: {self.rotation}, Direction: {direction}")