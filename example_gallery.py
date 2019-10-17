from ledtrix.screenfactory import create_screen, create_canvas
from ledtrix.apps.gallery import Gallery
from ledtrix.screen.abstractscreen import ScreenShapeRectangle
import config
import pygame
import time
import sys


from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.movingeffects import EffectRoll, EffectDiffusion
from ledtrix.effects.screeneffects import EffectBlinkConstantly, EffectComplementaryColor, EffectRotate


canvas = create_canvas(30, 40)
screen_effects = [
			#(EffectBlinkConstantly(frequency=1),{})
			#(EffectComplementaryColor(constant_color=True),{})
			(EffectRotate(speed=10),{})
			]

screen = create_screen(canvas=canvas, brightness=1, effects=screen_effects)
screen.shape.x0 = 20
screen.shape.y0 = 20

effects = [
			#(EffectRainbowTransformation(step_size=20),{})
			#(EffectRotate(speed=10),{})
			#(EffectDiffusion(speed=1),{})
			(EffectRoll(axis=(0,1,2), shift=(0,5,0)),{})
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
