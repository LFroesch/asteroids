import pygame
import sys
from constants import *
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import os

def main():
	os.environ['SDL_VIDEO_WINDOW_POS'] = "1920,0"
	pygame.init()
	print("Starting asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroid_field = AsteroidField(asteroids, updatable, drawable)
	asteroids.add(asteroid_field)
	updatable.add(player)
	updatable.add(asteroid_field)
	drawable.add(player)
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 36)
	high_score_file = "high_score.txt"
	try:
		with open(high_score_file, 'r') as file:
			high_score = int(file.read().strip())
	except (FileNotFoundError, ValueError):
		high_score = 0
	score = 0
	dt = 0

	while True:
		if score > high_score:
			high_score = score
			with open(high_score_file, 'w') as file:
				file.write(str(high_score))
		
		high_score_text = f"High Score: {high_score}"
		high_score_surface = font.render(high_score_text, True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect()
		margin = 10
		high_score_rect.topleft = (10, screen.get_height() - high_score_rect.height - margin)

		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
        			return
		screen.fill((0, 0, 0))		
		score_text = f"Score: {score}"
		score_surface = font.render(score_text, True, (255, 255, 255))
		text_rect = score_surface.get_rect()
		text_rect.topright = (screen.get_width() - 10, 10)
		player_shot = player.handle_input(dt)
		if player_shot:
			shots.add(player_shot)
			updatable.add(player_shot)
			drawable.add(player_shot)

		updatable.update(dt)
		for asteroid in asteroid_field.asteroids:
			if player.check_collision(asteroid):
				print("-----------------------------------------")
				print("- Game over!!!                          -")
				print(f"- Your score was {score}                    -")
				print("- type python3 main.py to play again :) -")
				print("-----------------------------------------")
				sys.exit()
		drawable.draw(screen)
		score += int(1)
		dt = (clock.tick(60) / 1000)
		screen.blit(high_score_surface, high_score_rect)
		screen.blit(score_surface, text_rect)
		pygame.display.flip()
		pygame.time.Clock().tick(60)
		
		

if __name__ == "__main__":
    main()
