from ledtrix.screenfactory import create_screen
from ledtrix.apps.gallery import Gallery
import config
import pygame
import time
import sys


from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.movingeffects import EffectRotate, EffectRoll, EffectDiffusion
from ledtrix.effects.screeneffects import EffectBlinkConstantly, EffectComplementaryColor

screen_effects = [
			#(EffectBlinkConstantly(frequency=1, minimum_brightness=0.1),{})
			(EffectComplementaryColor(constant_color=True),{})
			]
screen = create_screen(brightness=1, effects=screen_effects)
effects = [
			 (EffectRainbowTransformation(step_size=20),{})
			# (EffectRotate(speed=5),{})
			,(EffectDiffusion(speed=1),{})
			,(EffectRoll(axis=(0,1,2), shift=(0,1,0)),{})
			#,(EffectRainbowTransformation(step_size=20),{})
			#,(EffectRainbowTransformation(step_size=20),{})
		]

gallery = Gallery(screen, "examples/gallery/2", effects=effects)

while True:
	try:
		if config.virtual_hardware:
			pygame.time.wait(1)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.display.quit(), sys.exit()
		else:
			pass
	except KeyboardInterrupt:
		screen.clear()
		screen.update()
		break
