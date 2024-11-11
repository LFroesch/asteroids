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
	#pygame.quit()
	print("Game loop running")

	os.environ['SDL_VIDEO_DISPLAY'] = '1'
	os.environ['SDL_VIDEO_WINDOW_POS'] = '1920,0'
	
	screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

	pygame.init()
	print("Starting asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, screen)
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
	background = pygame.image.load("bg.png").convert()
	background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

	try:
		print(f"Attempting to open {high_score_file}")
		with open(high_score_file, 'r') as file:
			content = file.read().strip()
			print(f"File content: {content}")
			high_score = int(content)
	except (FileNotFoundError, ValueError) as e:
		print(f"Error loading high score: {e}")
		high_score = 0
	modifier = 1.0
	score = 0
	dt = 0
	kills = 0
	playing = True
	game_over = False

	while playing:

		if score > high_score:
			high_score = score
		
		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
        			return
		screen.fill((0, 0, 0))
		screen.blit(background, (0, 0))
		margin = 10
		screen_width = screen.get_width()
		screen_height = screen.get_height()
		
		modifier_text = f"Modifier: {modifier:,.2f}"
		modifier_surface = font.render(modifier_text, True, (255,255,255))
		modifier_rect = modifier_surface.get_rect()
		modifier_rect.topleft = (10, 10)

		kills_text = f"Kills: {kills:,}"
		kills_surface = font.render(kills_text, True, (255,255,255))
		kills_rect = kills_surface.get_rect()
		kills_rect.topleft = (10, modifier_rect.bottom + 5)

		score_text = f"Score: {score:,.0f}"
		score_surface = font.render(score_text, True, (255, 255, 255))
		text_rect = score_surface.get_rect()
		text_rect.topleft = (10, kills_rect.bottom + 5)

		high_score_text = f"High Score: {high_score:,.0f}"
		high_score_surface = font.render(high_score_text, True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect()
		high_score_rect.topleft = (margin, screen.get_height() - high_score_rect.height - margin)

		lives_text = f"Lives: {player.lives}"
		lives_surface = font.render(lives_text, True, (255, 255, 255))
		lives_rect = lives_surface.get_rect()
		lives_rect.topleft = (margin, text_rect.bottom + 5)

		player_shot = player.handle_input(dt)
		if player_shot:
			shots.add(player_shot)
			updatable.add(player_shot)
			drawable.add(player_shot)
		updatable.update(dt)
		asteroids.update(dt)

		
		# Check collision between player and asteroids
		asteroid_hits = pygame.sprite.spritecollide(player, asteroid_field.asteroids, True, pygame.sprite.collide_circle)
		# True means kill the asteroid on collision
		if asteroid_hits:  # If there were any collisions
			player.lives -= 1
			print("-----------------------------------------")
			print(f"|           -1 Life! -> {player.lives} Left          -")
			print("-----------------------------------------")
			if player.lives == 0:
				game_over = True
				playing = show_game_over_screen(screen, score, high_score, shots, asteroids, modifier, kills)

		for shot in shots:
			for asteroid in asteroid_field.asteroids:
				if shot.check_collision(asteroid):
					shot.kill()
					modifier += .05
					kills += 1
					if kills % 10 == 0:
						score += 5000 * modifier
					if kills % 20 == 0:
						modifier *= 1.5
					new_asteroids = asteroid.split()
					if new_asteroids:
						asteroids.add(new_asteroids)
						drawable.add(new_asteroids)
						updatable.add(new_asteroids)
						asteroid_field.add_asteroids(new_asteroids)
					pts_to_add = 100 * modifier
					score += pts_to_add
					print("-----------------------------------------")
					print(f"- You hit an asteroid! +{pts_to_add:.0f} pts -> {score:.0f}  -")
					print("-----------------------------------------")

		drawable.draw(screen)
		for sprite in drawable:
			sprite.draw(screen)
		score += int(1 * modifier)
		dt = (clock.tick(60) / 1000)
		screen.blit(high_score_surface, high_score_rect)
		screen.blit(score_surface, text_rect)
		screen.blit(modifier_surface, modifier_rect)
		screen.blit(kills_surface, kills_rect)
		screen.blit(lives_surface, lives_rect)
		pygame.display.flip()
		#pygame.time.Clock().tick(60)
		
def show_game_over_screen(screen, score, high_score, shots, asteroids, modifier, kills):
	print("-----------------------------------------")
	print("- Game over!!!                          -")
	print(f"- Your score was {score}                   -")
	print(f"- High score is {high_score}                    -")
	print("- type R to play again or Q to quit     -")
	print("-----------------------------------------")
	font_h = pygame.font.SysFont(None, 72)
	font_b = pygame.font.SysFont(None, 36)
	screen.fill((0, 0, 0))
	margin = 10
	save_high_score(high_score)

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

	high_score_text = f"High Score: {high_score:,.0f}"
	high_score_surface = font_b.render(high_score_text, True, (255, 255, 255))
	high_score_rect = high_score_surface.get_rect()
	high_score_rect.centerx = screen.get_width() // 2
	high_score_rect.top = game_over_subtext_rect.bottom + 20

	score_text = f"Score: {score:,.0f}"
	score_surface = font_b.render(score_text, True, (255 , 255, 255))
	text_rect = score_surface.get_rect()
	text_rect.centerx = screen.get_width() // 2
	text_rect.top = high_score_rect.bottom + 20

	modifier_text = f"Modifier: {modifier:,.2f}"
	modifier_surface = font_b.render(modifier_text, True, (255,255,255))
	modifier_rect = modifier_surface.get_rect()
	modifier_rect.centerx = screen.get_width() // 2
	modifier_rect.top = text_rect.bottom + 20

	kills_text = f"Kills: {kills:,}"
	kills_surface = font_b.render(kills_text, True, (255,255,255))
	kills_rect = kills_surface.get_rect()
	kills_rect.centerx = screen.get_width() // 2
	kills_rect.top = modifier_rect.bottom + 20

	screen.blit(high_score_surface, high_score_rect)
	screen.blit(score_surface, text_rect)
	screen.blit(modifier_surface, modifier_rect)
	screen.blit(kills_surface, kills_rect)
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

def save_high_score(high_score):
	high_score_file = "high_score.txt"
	try:
		with open(high_score_file, 'w') as file:
			file.write(str(int(high_score)))
	except Exception as e:
		print(f"Failed to save high score: {e}")


if __name__ == "__main__":
    main()
