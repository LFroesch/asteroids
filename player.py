from circleshape import CircleShape
from constants import *
import pygame
import math
import os
import sys
from shot import Shot, Shot2, Shot3

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		self.rotation = 0
		self.image = pygame.Surface((PLAYER_RADIUS*2, PLAYER_RADIUS*2), pygame.SRCALPHA)
		self.image.fill((255, 255, 255))  # White color
		self.rect = self.image.get_rect(center=(x, y))
		self.position = pygame.math.Vector2(x, y)
		self.draw_triangle()
		self.direction = pygame.Vector2(0,0)
		self.shoot_timer = 0
		self.lives = 3
	
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
		self.shoot_timer -= dt

	def handle_input(self, dt):
		new_shot = None
		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE]:
			new_shot = self.shoot2()
			if new_shot:
				pass
			#print(f"Shot fired from position: {self.position} with direction: {self.direction} and rotation: {self.rotation}")
		if keys[pygame.K_f]:
			new_shot = self.shoot()
			if new_shot:
				pass
		if keys[pygame.K_g]:
			new_shot = self.shoot3()
			if new_shot:
				pass
		if keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_q]:
			self.rotation -= PLAYER_TURN_SPEED * dt
		if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_e]:
			self.rotation += PLAYER_TURN_SPEED * dt
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			self.move(dt)
		if keys[pygame.K_s] or keys [pygame.K_DOWN]:
			self.move(-dt)
		if keys[pygame.K_ESCAPE]:
			sys.exit()
		return new_shot
	
	def shoot(self):
		#Create and return a shot instance located at the player's position
		if self.shoot_timer > 0:
			return
		new_shot = Shot(self.position.x, self.position.y, self.rotation)
		self.shoot_timer = .1
		return new_shot
	
	def shoot2(self):
		#Create and return a shot2 (BIG BULLET) instance located at the player's position
		if self.shoot_timer > 0:
			return
		new_shot = Shot2(self.position.x, self.position.y, self.rotation)
		self.shoot_timer = .1
		return new_shot
	
	def shoot3(self):
		#Create and return a shot3 (SMALL BULLET) instance located at the player's position
		if self.shoot_timer > 0:
			return
		new_shot = Shot3(self.position.x, self.position.y, self.rotation)
		self.shoot_timer = .1
		return new_shot
		
		

	def update_graphics(self):
		self.draw_triangle()
		self.rect.center = self.position

	def move(self, dt):
		self.direction = pygame.Vector2(math.sin(math.radians(self.rotation)), 
                               -math.cos(math.radians(self.rotation)))
		self.position += self.direction * PLAYER_SPEED * dt
		#print(f"Rotation: {self.rotation}, Direction: {direction}")