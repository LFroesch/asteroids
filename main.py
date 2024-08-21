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
	print("Game loop running")
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
	playing = True
	game_over = False

	while playing:

		if score > high_score:
			high_score = score
			with open(high_score_file, 'w') as file:
				file.write(str(high_score))
		
		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
        			return
		screen.fill((0, 0, 0))

		high_score_text = f"High Score: {high_score}"
		high_score_surface = font.render(high_score_text, True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect()
		margin = 10
		high_score_rect.topleft = (10, screen.get_height() - high_score_rect.height - margin)		
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
		asteroids.update(dt)

		
		for asteroid in asteroid_field.asteroids:
			if player.check_collision(asteroid):
				game_over = True
				playing = show_game_over_screen(screen, score, high_score, shots, asteroids)
				#print("-----------------------------------------")
				#print("- Game over!!!                          -")
				#print(f"- Your score was {score}                    -")
				#print(f"- High score is {high_score}                    -")
				#print("- type python3 main.py to play again :) -")
				#print("-----------------------------------------")
				#sys.exit() #hashedout to work on game_over_screen
		

		for shot in shots:
			for asteroid in asteroid_field.asteroids:
				if shot.check_collision(asteroid):
					shot.kill()
					new_asteroids = asteroid.split()
					if new_asteroids:
						asteroids.add(new_asteroids)
						drawable.add(new_asteroids)
						updatable.add(new_asteroids)
						asteroid_field.add_asteroids(new_asteroids)
					score += 100
					print("-----------------------------------------")
					print(f"- You hit an asteroid! +100 pts -> {score}  -")
					print("-----------------------------------------")

		drawable.draw(screen)
		score += int(1)
		dt = (clock.tick(60) / 1000)
		screen.blit(high_score_surface, high_score_rect)
		screen.blit(score_surface, text_rect)
		pygame.display.flip()
		pygame.time.Clock().tick(60)
		
def show_game_over_screen(screen, score, high_score, shots, asteroids):
	font_h = pygame.font.SysFont(None, 72)
	font_b = pygame.font.SysFont(None, 36)
	screen.fill((0, 0, 0))
	margin = 10

	game_over_text = "GAME OVER!"
	game_over_text_surface = font_h.render(game_over_text, True, (255, 255, 255))
	game_over_text_rect = game_over_text_surface.get_rect()
	game_over_text_rect.centerx = screen.get_width() // 2
	game_over_text_rect.centery = screen.get_height() // 2 - 50  # Adjust this value as needed

	game_over_subtext = "Press R button to Restart, or Q to quit"
	game_over_subtext_surface = font_b.render(game_over_subtext, True, (255, 255, 255))
	game_over_subtext_rect = game_over_subtext_surface.get_rect()
	game_over_subtext_rect.centerx = screen.get_width() // 2
	game_over_subtext_rect.top = game_over_text_rect.bottom + 20

	high_score_text = f"High Score: {high_score}"
	high_score_surface = font_b.render(high_score_text, True, (255, 255, 255))
	high_score_rect = high_score_surface.get_rect()
	high_score_rect.topleft = (10, screen.get_height() - high_score_rect.height - margin)

	score_text = f"Score: {score}"
	score_surface = font_b.render(score_text, True, (255 , 255, 255))
	text_rect = score_surface.get_rect()
	text_rect.topright = (screen.get_width() - 10, 10)

	screen.blit(high_score_surface, high_score_rect)
	screen.blit(score_surface, text_rect)
	screen.blit(game_over_text_surface, game_over_text_rect)
	screen.blit(game_over_subtext_surface, game_over_subtext_rect)
	pygame.display.flip()
	
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_r:
					reset_game(shots, asteroids)
					return True
					
				elif event.key == pygame.K_q:
					sys.exit()
	pygame.quit()

def reset_game(shots, asteroids):
	print("Restting field")
	shots.empty()
	asteroids.empty()
	main()

if __name__ == "__main__":
    main()
