from ledtrix.screenfactory import create_screen, create_canvas
from ledtrix.apps.gallery import Gallery
from ledtrix.screen.abstractscreen import ScreenShapeRectangle, AbstractScreen
import ledtrix.images as images
import config
import pygame
import time
import sys
import numpy as np
from PIL import Image


from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.movingeffects import  EffectDiffusion
from ledtrix.effects.screeneffects import EffectRoll, EffectBlinkConstantly, EffectComplementaryColor, EffectRotate, EffectChangeBrighness, EffectOverlay, EffectFlipAxis
from ledtrix.triggers.triggers import TriggerChangeDirection, TriggerExponentialDecay, TriggerUpAndDown

tick_interval = 0.001
trigger_change_rotation_direction = TriggerChangeDirection()
trigger_flip = TriggerChangeDirection()
trigger_blink = TriggerUpAndDown(lifetime=0.5, max_multiplier=100)

canvas_main = create_canvas(30, 40)
canvas_side = create_canvas(30, 40)

#canvas_side.set_pixels(images.get_image_array('examples/pictures/guy.png'))

screen_effects_side = [
			(EffectRotate(speed=1, pivot=[15,15]),{})
			,(EffectRoll(axis=(0,1,2), shift=(1,0,0)),{})
			#,(EffectBlinkConstantly(frequency=0.5),{})
				]

screen_side = create_screen(canvas=canvas_side, brightness=1, effects=screen_effects_side, abstract=True)

screen_effects = [
			#(EffectChangeBrighness(brightness=0.2, triggers=[trigger_blink]), {})
			(EffectRoll(axis=(0,1,2), shift=(-1,0,0)),{})
			,(EffectOverlay(screen_side, alpha=0.01, triggers=[trigger_blink]),{})
			,(EffectFlipAxis(axis=(0,1), triggers=[trigger_flip]),{})
			#,(EffectBlinkConstantly(frequency=0.5),{})
			]

screen_main = create_screen(canvas=canvas_main, brightness=1, effects=screen_effects)

effects = [
			#(EffectDiffusion(speed=1),{})
			#,(EffectRoll(axis=(0,1,2), shift=(1,0,0)),{})
		]
print(screen_side)
print(screen_main)
gallery = Gallery(screen_main, "examples/gallery/1", effects=effects, adjust_canvas=True)
gallery2 = Gallery(screen_side, "examples/gallery/2", effects=effects, adjust_canvas=False)




from pygame.locals import QUIT, KEYDOWN, KEYUP
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
going = True
while going:
	time.sleep(tick_interval)
	screen_side.update()
	gallery.tick()
	gallery2.tick()
	try:
		events = event_get()
		for e in events:
			if e.type in [QUIT]:
				going = False
				pygame.display.quit(), sys.exit()
			if e.type in [KEYUP]:
				trigger_change_rotation_direction.trigger()
				trigger_blink.trigger()
				trigger_flip.trigger()
		
	except KeyboardInterrupt:
		screen_main.clear()
		screen_main.update()
		pygame.display.quit(), sys.exit()
		break
