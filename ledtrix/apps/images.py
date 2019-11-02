import time
from ledtrix.apps import Module
from ledtrix.images import gif_to_arrays

class ImageGIF(Module):
	def __init__(self, screen, filepath, tick_interval, effects=None):
		self.screen = screen
		self.filepath = filepath
		self.tick_interval = tick_interval
		if effects is None:
			self.effects = []
		else:
			self.effects = effects
		# intialize last process timestamp
		self.last_processed = time.time()
		self.pos = 0

		# Load arrays
		self.load_arrays()
		self.pixel = self.arrays[0]

	def load_arrays(self):
		self.arrays = gif_to_arrays(self.filepath)

	def tick(self):
		if time.time() > self.last_processed + self.tick_interval:
			# Load next array
			self.pos = (self.pos + 1) % len(self.arrays)
			self.pixel = self.arrays[self.pos]
			self.screen.canvas.clear()
			self.screen.canvas.set_pixels(self.pixel)
			self.process_effects()
			self.screen.update() 
			self.screen.update()
			self.last_processed = time.time()
