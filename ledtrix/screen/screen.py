import pygame
import config
from ledtrix.screen.abstractscreen import AbstractScreen, ScreenShapeRectangle
from ledtrix.helpers import darken_color

instance = None

class Screen(AbstractScreen):
	def __init__(self, canvas, width = 16, height = 16, led_pin = 18, led_freq_hz = 800000, led_dma = 5, led_invert = False, led_brightness = 0.5, effects=[]):
		super(Screen, self).__init__(canvas=canvas, shape=ScreenShapeRectangle(width, height), brightness=brightness, effects=effects)
		import neopixel
		import board
		self.strip = neopixel.NeoPixel(board.D18, width * height, auto_write=False, brightness=led_brightness)
		self.effects=effects
		global instance
		instance = self	
	
	def update(self):
		print("creating screen sized x={}, y={}".format(self.shape.width, self.shape.height))	
		print("Image size: ", len(self.pixel), len(self.pixel[0]))
		for y in range(self.shape.height):
			for x in range(self.shape.width):
				if x <= len(self.pixel)-1 and y <= len(self.pixel[0]) -1:
					color = darken_color(self.pixel[x][y], self.brightness)
					if y % 2 == 0:
						self.strip[y * self.shape.width + x] = color
					else: self.strip[y * self.shape.width + self.shape.width - 1 - x] = color
		self.strip.show()

	def update_brightness(self):
		self.strip.brightness = int(4 + 3.1 * (config.brightness + 1)**2)

	def set_brightness(self, value):
		value = min(max(value, 0), 0.5)
		config.brightness = value
		self.update_brightness()
		config.store()

	def get_brightness(self):
		return config.brightness
