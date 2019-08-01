import sys
from ledtrix.screenfactory import create_screen
from ledtrix.apps.snake import Snake
import time
import config
import pygame
import ledtrix.input

screen = create_screen()

snake = Snake(screen)
snake.start()

while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit(), sys.exit()
		else:
			ledtrix.input.tick()