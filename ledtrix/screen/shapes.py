
"""Screen shapes
"""
class ScreenShapeAbstract:
	def __init__(self, pixel_mapping):
		self.pixel_mapping = pixel_mapping
		self.length = len(pixel_mapping)

	def __getitem__(self, index):
		"""Custom indexing
		"""
		# convert a simple index x[y] to a tuple for consistency
		return self.pixel_mapping[index]

	def __len__(self):
		"""Custom length
		"""	
		return len(self.pixel_mapping)
	


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
		self.pixel_mapping = self._get_pixel_mapping()
		# Create ScreenShapeAbstract object
		super(ScreenShapeRectangle, self).__init__(pixel_mapping=self.pixel_mapping)

	def _get_pixel_coordinate(self, pixel_index):
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
		return (self.x0 + x_screen, self.y0 + y_screen)

	def _get_pixel_mapping(self):
		"""Gets whole mapping of all pixels

		Returns
		-------
		dict[int:tuple(int,int)]
			Dictionary where each mixel is mapped to underlying coordinate.
		"""
		dict = {}
		for pixel_index in range(self.width * self.height):
			dict[pixel_index] = self._get_pixel_coordinate(pixel_index)
		return dict
