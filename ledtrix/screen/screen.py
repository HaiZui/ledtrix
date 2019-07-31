import pygame
import config
from ledtrix.screen.abstractscreen import AbstractScreen

instance = None

class Screen(AbstractScreen):
	def __init__(self, width = 16, height = 16, led_pin = 18, led_freq_hz = 800000, led_dma = 5, led_invert = False, led_brightness = 0.5):
		super(Screen, self).__init__(width, height)
		import neopixel
		import board
		self.strip = neopixel.NeoPixel(board.D18, width * height, auto_write=False, brightness=led_brightness)
		
		global instance
		instance = self	
	
	def update(self):
		print("createing screen sized x={}, y={}".format(self.width, self.height))	
		print("Image size: ", len(self.pixel), len(self.pixel[0]))
		for y in range(self.height):
			for x in range(self.width):
				if y <= len(self.pixel)-1 and x <= len(self.pixel[0]) -1:
					if y % 2 == 0:
						self.strip[y * self.width + x] = self.pixel[self.height-y-1][x]
					else: self.strip[y * self.width + self.width - 1 - x] = self.pixel[self.height-y-1][x]
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
