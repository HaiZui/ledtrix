from ledtrix.screenfactory import create_screen
from ledtrix.apps.gallery import Gallery
import config
import pygame
import time
import sys


from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.movingeffects import EffectRotate, EffectRoll

effects = [
			(EffectRoll(axis=(0,1,2), shift=(2,2,0)),{})
			,(EffectRainbowTransformation(step_size=20),{})
		]
screen = create_screen()

gallery = Gallery(screen, "examples/gallery", effects=effects)

while True:
	if config.virtual_hardware:
		pygame.time.wait(1)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit(), sys.exit()
	else:
		time.sleep(0.01)
