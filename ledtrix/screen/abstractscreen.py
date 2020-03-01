import numpy as np

class AbstractScreen(object):
	def __init__(self, shape, canvas, brightness=1, effects=[]):
		"""Abstract screen class
		
		Arguments
		---------
		shape:
		"""
		self.shape = shape
		self.canvas = canvas
		canvas.add_screen(self)
		self.brightness = min(brightness, 1)
		self.effects = effects

	def __iter__(self):
		"""Iterates through pixels and returns absolute coordinate and color value
		"""
		return AbstractScreenIterator(self)

	def update(self):
		self.process_effects()

	def initialize_effects(self):
		for effect, _ in self.effects:
			effect.initialize()

	def process_effects(self):
		for effect, kwargs in self.effects:
			effect.process(self, **kwargs)

	def process_triggers(self):
		for effect, kwargs in self.effects:
			effect.trigger(self, **kwargs)

	def adjust_pixel_mapping(self):
		self.shape.pixel_mapping_absolute = self.shape.pixel_mapping_absolute % np.array([self.canvas.width, self.canvas.height])

class AbstractScreenIterator:
	def __init__(self, screen):
		self._screen = screen
		self._index = 0

	def __next__(self):
		"""Iterates through pixels and returns absolute coordinate and color value
		"""
		if self._index < self._screen.shape.length:
			coordinate_relative = self._screen.shape.pixel_mapping_relative[self._index]
			coordinate_absolute = self._screen.shape.pixel_mapping_absolute[self._index]
			value = self._screen.canvas[coordinate_absolute] * self._screen.brightness
			self._index += 1
			return coordinate_relative, coordinate_absolute, value
		# End of Iteration
		raise StopIteration