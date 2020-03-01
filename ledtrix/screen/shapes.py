
"""Screen shapes
"""
import numpy as np

class ScreenShapeAbstract:
	def __init__(self, pixel_mapping):
		self.pixel_mapping = pixel_mapping
		self.length = len(pixel_mapping)

	def __getitem__(self, index):
		"""Custom indexing
		Gets pixel coordinate in the absolute coordinate system
		"""
		# convert a simple index x[y] to a tuple for consistency
		return self.pixel_mapping[index]

	def __len__(self):
		"""Custom length 
		Represents number of pixels
		"""	
		return len(self.pixel_mapping)
	
	def get_minimum_bounding_box_from_origin(self):
		"""Get minimum box fitting the entire shape including also absolute origin.
		Note that negative numbers are neglected.
		"""
		return self.pixel_mapping.max(axis=0)
	
	def get_minimum_bounding_box_size(self):
		maxes = self.pixel_mapping_relative.max(axis=0)
		mins = self.pixel_mapping_relative.min(axis=0)
		return maxes-mins


class ScreenShapeRectangle(ScreenShapeAbstract):
	def __init__(self, width, height, origin=(0,0), parallel_rows=False):
		"""Represents rectangle

		Arguments
		---------
		width: int
			Width in pixels
		height: int
			Height in pixels
		origin: tuple(int, int)
			Origin of the rectangle
		parallel_rows: bit
			False = each sequential row is reversed compared to the previous
			True = each row is parallel
		"""
		self.width = width
		self.height = height
		self.x0 = origin[0]
		self.y0 = origin[1]
		self.origin = origin
		self.parallel_rows = parallel_rows
		# Initialize mapping of pixels
		self.pixel_mapping_absolute = self._get_pixel_mapping(relative=False)
		self.pixel_mapping_relative = self._get_pixel_mapping(relative=True)
		# Create ScreenShapeAbstract object
		super(ScreenShapeRectangle, self).__init__(pixel_mapping=self.pixel_mapping_absolute)

	def _get_pixel_coordinate(self, pixel_index, relative=False):
		"""Find coordinate of the pixel
		
		(x, y) -> pixel_number
		
		Returns
		-------
		coordinate: tuple(int, int)
			Coordinate of the pixel
		"""
		x_screen = pixel_index % self.width
		y_screen = int(pixel_index/self.width)
		if self.parallel_rows is False and y_screen%2==1:
			x_screen = self.width - x_screen -1
		if relative is False:
			x0 = self.x0
			y0 = self.y0
		else:
			x0 = 0
			y0 = 0
		return (x0 + x_screen, y0 + y_screen)

	def _get_pixel_mapping(self, relative=False):
		"""Gets whole mapping of all pixels

		Returns
		-------
		dict[int:tuple(int,int)]
			Dictionary where each mixel is mapped to underlying coordinate.
		"""
		array = np.array(self._get_pixel_coordinate(0, relative=relative))
		for pixel_index in range(1, self.width * self.height):
				coord = np.array(self._get_pixel_coordinate(pixel_index, relative=relative))
				array = np.vstack((array, coord))
		return array
