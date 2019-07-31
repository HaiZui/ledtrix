# Use python 3.x
from time import sleep, time
import random
import argparse
import numpy as np

import board
import neopixel

import effects as eff

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)



# New module
def combine_pixels(pixels, pixels_other):
	pixels_return = pixels
	for i in range(len(pixels)):
		if np.all(pixels_other[i] == (0,0,0)):
			pixels_return[i] = pixels[i]
		elif np.all(pixels[i] == (0,0,0)):
			pixels_return[i] = pixels_other[i]
		else:
			pixels_return[i] = pixels[i]
	return pixels_return

class EffectCollection:
	def __init__(self, pixels, effects=[]):
		self.pixels = pixels
		self.effects = effects

		# Store pixels also in numpy array format to speed things up
		# This way pixels do not need to be updated continuously
		# and only true modifications are updated
		self.pixels_list = np.array(list(pixels))		
		self.n = pixels.n
		
	def add_effect(self, effect, relative_speed=1):
		self.effects.append(effect)

	def advance(self):
		pixels_list_old = self.pixels_list.copy()
		# Clear pixels_list. Note that pixels will be updated only if necessary
		self.clear()
		pixels_list_new = self.pixels_list.copy()
		for effect_i in range(len(self.effects)):
			effect_cur = self.effects[effect_i]
			effect_cur.advance()
			pixels_appended = effect_cur.pixels.copy()
			pixels_list_new = combine_pixels(pixels_appended, pixels_list_new)
		# Detect changes to pixels and update
		self.update_pixels(pixels_list_old, pixels_list_new)
		self.pixels_list = pixels_list_new

	def update_pixels(self, pixels_list_old, pixels_list_new):
		is_updated = pixels_list_old != pixels_list_new
		for pixel_i in range(self.n):
			if np.any(is_updated[pixel_i]) == True:
				self.pixels[pixel_i] = pixels_list_new[pixel_i]
	def show(self):
		self.pixels.show()

	def clear(self):
		self.pixels_list = np.array([(0,0,0)] * self.n)
		
	def clear_effects(self):
		for effect in self.effects:
			effect.clear()

	def showtime(self, runtime=None):
		try:
			# Max time 60 seconds
			runtime = runtime or 60
			endtime = time() + runtime
			while endtime > time():
				print(self.pixels)
				self.show()
				self.advance()
			self.clear()
			self.pixels.fill((0,0,0))
			self.show()
		except KeyboardInterrupt:
			self.clear()
			self.pixels.fill((0,0,0))
			self.show()
			pass

class EffectCollection_depr:
	def __init__(self, pixels, effects=[], speeds=[]):
		self.pixels = pixels
		self.effects = effects
		
		if len(speeds) == len(effects):
			self.speeds = speeds
		else:
			self.speeds = [1 for i in range(len(effects))]
			
		# Initialize step
		self.step = 0
	

	def add_effect(self, effect, relative_speed=1, kwargs=None):
		self.effects.append((effect, kwargs))
		self.speeds.append(relative_speed)

	def calculate_pixels_at_step(self, step):
		self.clear()
		pixels = self.pixels
		for effect_i in range(len(self.effects)):
			step_cur = int(self.speeds[effect_i] * step)
			effect_cur, kwargs_cur = self.effects[effect_i]
			pixels_cur = effect_cur.func(step_cur, pixels, **kwargs_cur)
			if isinstance(effect_cur, ModifyingEffect):
				pixels = pixels_cur
			elif isinstance(effect_cur, AppendingEffect):
				pixels = self._combine_pixels(pixels_cur, pixels)
				
		return pixels

	def _combine_pixels(self, pixels, pixels_other):
		pixels_return = pixels
		for i in range(pixels.n):
			if pixels_other[i] == (0,0,0):
				pixels_return[i] = pixels[i]
			elif pixels[i] == (0,0,0):
				pixels_return[i] = pixels_other[i]
			else:
				pixels_return[i] = pixels[i]
		return pixels
			

	def jump_to_step(self, step):
		self.pixels = self.calculate_pixels_at_step(step)
	
	def calculate_pixels(self):
		pixels = self.calculate_pixels_at_step(self.step)
		return pixels
	
	def advance(self):
		self.step += 1
	
	def show(self):
		self.pixels.show()

	def clear(self):
		self.pixels.fill((0,0,0))

	def showtime(self):
		try:
			while True:
				print(self.pixels)
				self.calculate_pixels()
				self.show()
				self.advance()				

		except KeyboardInterrupt:
			self.clear()
			self.show()
			pass
			

# TODO
class Pixels:
	def __init__(self, n):
		self.n = n
		self.pixels_array = np.array([(0,0,0)] * n)
		
	def show(self):
		pass
