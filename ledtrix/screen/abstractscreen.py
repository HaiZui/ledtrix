import ledtrix.helpers as helpers
import time
import copy
import numpy as np

class ScreenShapeRectangle:
	def __init__(self, width, height,x0=0, y0=0):
		self.width = width
		self.height = height
		self.x0 = x0
		self.y0 = y0


class ScreenShapeCircle:
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius

class AbstractScreen(object):
	def __init__(self, shape, canvas, scale=1, brightness=1, effects=[]):
		self.shape = shape
		self.canvas = canvas
		self.scale = scale
		self.brightness = brightness
		self.effects = effects
		self._crop_canvas()

	def _crop_canvas(self):
		width = self.shape.width
		height = self.shape.height
		x0 = self.shape.x0
		y0 = self.shape.y0
		self.pixel = np.roll(self.canvas.pixel, axis=(0,1,2), shift=(-x0,-y0,0))[:width,:height]

	def clear(self, color = (0,0,0)):
		for x in range(len(self.pixel)):
			for y in range(len(self.pixel[0])):				
				self.pixel[x][y] = color

	def update(self):
		print('screen update')
		self._crop_canvas()
		self.process_effects()
		pass

	def initialize_effects(self):
		for effect, _ in self.effects:
			effect.initialize()

	def process_effects(self):
		for effect, kwargs in self.effects:
			effect.process(self, **kwargs)

	def process_triggers(self):
		for effect, kwargs in self.effects:
			effect.trigger(self, **kwargs)
