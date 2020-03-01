import numpy as np

from ledtrix.helpers import add_image_arrays

class Canvas(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		# Initialize pixels
		self.pixel = np.array([[(0,0,0) for y in range(height)] for x in range(width)])

	def __getitem__(self, indices):
		# convert a simple index x[y] to a tuple for consistency
		if not isinstance(indices, tuple):
			indices = tuple(indices)
		return self.pixel[indices]

	def clear(self):
		self.pixel.fill(0)

	def set_pixels(self, array, pos=(0,0), overwrite=False, opacity=1):
		"""Sets image to canvas

		Arguments
		---------
		array: np.array
			Image array
		pos: tuple(int, int)
			Lower left corner of the image position
		overwrite: boolean
			True = canvas pixels is replaced by new image
		"""
		if overwrite is False:
			self.pixel = add_image_arrays(array_1=self.pixel, array_2=array, pos=pos, opacity=opacity)
		else:
			self.pixel = array
			self.height = array.shape[0]
			self.width = array.shape[1]

		