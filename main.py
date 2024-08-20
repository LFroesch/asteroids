import pygame
from constants import *
from circleshape import *
from player import *

def main():
	pygame.init()
	print("Starting asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	updatable = pygame.sprite.Group()
	updatable.add(player)
	drawable= pygame.sprite.Group()
	drawable.add(player)
	clock = pygame.time.Clock()
	dt = 0
	while True:
		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
        			return
		screen.fill((0, 0, 0))
		updatable.update(dt)
		drawable.draw(screen)
		pygame.display.flip()
		dt = (clock.tick(60) / 1000)

if __name__ == "__main__":
    main()
