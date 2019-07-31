from ledtrix.screenfactory import create_screen
from ledtrix.apps.gallery import Gallery
import config
import pygame
import time
import sys

screen = create_screen()

gallery = Gallery(screen, "examples/gallery")

while True:
	if config.virtual_hardware:
		pygame.time.wait(1)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit(), sys.exit()
	else:
		time.sleep(0.01)
