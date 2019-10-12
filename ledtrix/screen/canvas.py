import numpy as np

from ledtrix.helpers import add_image_arrays

class Canvas(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.pixel = np.array([[(0,0,0) for y in range(height)] for x in range(width)])

	def clear(self):
		self.pixel.fill(0)

	def set_pixels(self, array, pos=(0,0)):
		self.pixel = add_image_arrays(array_1=self.pixel, array_2=array, pos=pos)