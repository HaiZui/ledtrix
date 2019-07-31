from screenfactory import create_screen
from modules.clock import Clock
import config
import time
import pygame
import sys

screen = create_screen()

clock = Clock(screen)
clock.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit(), sys.exit()
	else:
		time.sleep(0.01)