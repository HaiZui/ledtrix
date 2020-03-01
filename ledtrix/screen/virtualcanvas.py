import pygame
import numpy as np

from ledtrix.screen.canvas import Canvas

class VirtualCanvas(Canvas):
	def __init__(self, pixel_size=15):
		self.pixel_size = pixel_size
		self.screens = []
		# Initialize size
		self.width = 0
		self.height = 0
		# Initialize Canvas
		super(VirtualCanvas, self).__init__(width=self.width, height=self.height)

	def _get_upper_right(self):
		if len(self.screens) > 0:
			maxes = tuple(i.shape.get_minimum_bounding_box_from_origin() for i in self.screens)
			upper_right = np.vstack(maxes).max(axis=0)
		else:
			upper_right = np.array([0,0])
		return upper_right

	def add_screen(self, screen):
		# Set origin of the new screen
		self.screens.append({'screen':screen, 'origin':np.array([self.width,0])})
		# New size of the canvas
		screen_size = screen.shape.get_minimum_bounding_box_size()
		# Add new screen to the right of the previous one
		self.width += screen_size[0]
		self.height = max(self.height, screen_size[1])
        # Initialize pygame screen
		pygame.display.init()
		self.screen = pygame.display.set_mode([self.width * self.pixel_size, self.height * self.pixel_size], 0)
		self.surface = pygame.Surface(self.screen.get_size())


	def update(self):
		for i in self.screens:
			screen = i['screen']
			origin = i['origin']
			screen.process_effects()
			# Iterate over pixels and draw them according to mapping
			for pos_relative, _ , color in screen:
				x_coor = origin[0] + pos_relative[0]
				y_coor = origin[1] + pos_relative[1]
				pygame.draw.rect(self.surface, color, (x_coor * self.pixel_size, y_coor * self.pixel_size, self.pixel_size, self.pixel_size))

		# Finally, update the whole screen by processin
		# Flip vertically (pygame defines origin at the top left corner, we want to transform it to lower left corner)
		self.screen.blit(pygame.transform.flip(self.surface, False, True), (0, 0))
		pygame.display.flip()
	
