from ledtrix.screenfactory import create_screen, create_canvas
from ledtrix.apps.gallery import Gallery
from ledtrix.screen.abstractscreen import ScreenShapeRectangle
import config
import pygame
import time
import sys


from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.movingeffects import EffectRoll, EffectDiffusion
from ledtrix.effects.screeneffects import EffectBlinkConstantly, EffectComplementaryColor, EffectRotate, EffectChangeBrighness
from ledtrix.triggers.triggers import TriggerChangeDirection, TriggerExponentialDecay, TriggerUpAndDown

trigger_change_rotation_direction = TriggerChangeDirection()
trigger_blink = TriggerUpAndDown(lifetime=0.2, max_multiplier=10)

canvas = create_canvas(30, 40)
screen_effects = [
			#(EffectBlinkConstantly(frequency=1),{})
			#(EffectRotate(speed=10, triggers=[trigger_change_rotation_direction]),{})
			(EffectChangeBrighness(brightness=0.1, triggers=[trigger_blink]), {})
			,(EffectComplementaryColor(constant_color=False),{})
			]

screen = create_screen(canvas=canvas, brightness=0.1, effects=screen_effects)
screen.shape.x0 = 0
screen.shape.y0 = 15

gallery_effects = [
			#(EffectRainbowTransformation(step_size=20),{})
			#(EffectColorTransformation(angle=10),{})
			#(EffectDiffusion(speed=2),{})
			(EffectRoll(axis=(0,1,2), shift=(0,1,0), randomize_direction=True),{})
		]

gallery = Gallery(screen, "examples/gallery/2", effects=gallery_effects, adjust_canvas=True)


from pygame.locals import QUIT, KEYDOWN, KEYUP
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
going = True
while going:
	try:
		events = event_get()
		for e in events:
			if e.type in [QUIT]:
				going = False
				pygame.display.quit(), sys.exit()
			if e.type in [KEYUP]:
				trigger_change_rotation_direction.trigger()
				trigger_blink.trigger()
		
	except KeyboardInterrupt:
		screen.clear()
		screen.update()
		pygame.display.quit(), sys.exit()
		break
