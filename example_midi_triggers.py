from ledtrix.screenfactory import create_screen
from ledtrix.apps.gallery import Gallery
import config
import pygame
import pygame.midi
import time
import sys

from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.movingeffects import EffectRotate, EffectRoll, EffectDiffusion
from ledtrix.effects.screeneffects import EffectBlinkConstantly, EffectExponentialFade


# Initialize pygame
pygame.init()
pygame.midi.init()

screen_effects = [
			(EffectExponentialFade(lifetime=100),{})
			]
screen = create_screen(brightness=0.1, effects=screen_effects)
effects = [
			# (EffectRainbowTransformation(step_size=20),{})
			#(EffectRotate(speed=10),{})
			(EffectDiffusion(speed=10),{})
			,(EffectRoll(axis=(0,1,2), shift=(1,3,0)),{})
			,(EffectRainbowTransformation(step_size=20),{})
			#,(EffectRainbowTransformation(step_size=20),{})
		]

gallery = Gallery(screen, "examples/gallery/2", effects=effects)

midi_input = pygame.midi.Input(1)


from pygame.locals import QUIT, KEYDOWN
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
going = True
while going:
	events = event_get()
	for e in events:
		if e.type in [QUIT]:
			going = False
		if e.type in [KEYDOWN]:
			going = False
		if e.type in [pygame.midi.MIDIIN]:
			screen.process_triggers()

	if midi_input.poll():
		midi_events = midi_input.read(10)
		# convert them into pygame events.
		midi_evs = pygame.midi.midis2events(midi_events, midi_input.device_id)

		for m_e in midi_evs:
			event_post( m_e )
del midi_input
pygame.midi.quit()

# while True:
# 	if inp.poll():
# 		print('Triggered')
# 		screen.brightness = 1
# 	pygame.time.wait(1)
# 	try:
# 		if config.virtual_hardware:
# 			pygame.time.wait(1)
# 			for event in pygame.event.get():
# 				print(event)
# 				if event.type == pygame.QUIT:
# 					pygame.display.quit(), sys.exit()		
# 			screen.brightness = 0.1
# 		else:
# 			screen.brightness = 0.1
# 			pass
# 	except KeyboardInterrupt:
# 		screen.clear()
# 		screen.update()
# 		break
