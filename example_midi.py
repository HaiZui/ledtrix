

import pygame
import pygame.midi
from pygame.locals import QUIT, KEYDOWN

# Initialize pygame
pygame.init()
pygame.midi.init()

pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.display.set_mode((1,1))
going = True
i = pygame.midi.Input(1)
while going:
	events = event_get()
	for e in events:
		if e.type in [QUIT]:
			going = False
		if e.type in [KEYDOWN]:
			going = False
		if e.type in [pygame.midi.MIDIIN]:
			print (e, e.data1)

	if i.poll():
		print('polled')
		midi_events = i.read(10)
		# convert them into pygame events.
		midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

		for m_e in midi_evs:
			event_post( m_e )

del i
pygame.midi.quit()