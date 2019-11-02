
import pygame
import pygame.midi as pygame_midi
from pygame.locals import QUIT







# Initialize pygame
pygame.init()
pygame.midi.init()

midi_input = pygame.midi.Input(1)

print("Found {} midi devices".format(pygame_midi.get_count()))

for i in range(pygame_midi.get_count()):
    print("#{}: {}".format(i, pygame_midi.get_device_info(i)))


midi_input_id = pygame_midi.get_default_input_id()

midi_input_id = 2
midi_input = pygame_midi.Input(midi_input_id)

print("Using input #{}".format(midi_input_id))


pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
going = True
while going:
	# Check for keypresses
	for event in pygame.event.get():
		if event.type in [QUIT]:
			going = False

	if midi_input.poll():
		midi_events = midi_input.read(40)
		# convert them into pygame events.
		midi_evs = pygame.midi.midis2events(midi_events, midi_input.device_id)
		for event in midi_evs:
			print(event)

del midi_input
pygame.midi.quit()