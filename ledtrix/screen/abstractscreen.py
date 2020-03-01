
class AbstractScreen(object):
	def __init__(self, shape, canvas, brightness=1, effects=[]):
		"""Abstract screen class
		
		Arguments
		---------
		shape:
		"""
		self.shape = shape
		self.canvas = canvas
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

class AbstractScreenIterator:
	def __init__(self, screen):
		self._screen = screen
		self._index = 0

	def __next__(self):
		"""Iterates through pixels and returns absolute coordinate and color value
		"""
		if self._index < self._screen.shape.length:
			coordinate = self._screen.shape.pixel_mapping[self._index]
			value = self._screen.canvas[coordinate] * self._screen.brightness
			self._index += 1
			return coordinate, value
		# End of Iteration
		raise StopIteration