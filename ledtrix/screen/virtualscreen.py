import pygame
import collections
from ledtrix.screen.abstractscreen import AbstractScreen
from ledtrix.screen.shapes import ScreenShapeRectangle
from ledtrix.helpers import darken_color
from PIL import Image

class VirtualScreen(AbstractScreen):
	def __init__(self, canvas, shape, brightness=1, effects=[], pixel_size=15):	
		super(VirtualScreen, self).__init__(canvas=canvas, shape=shape, brightness=brightness, effects=effects)
		self.pixel_size = pixel_size
		# Initialize pygame window
		pygame.display.init()
		self.screen = pygame.display.set_mode([canvas.width * self.pixel_size, canvas.height * self.pixel_size], 0)
		self.surface = pygame.Surface(self.screen.get_size())	
				
	def update(self):
		self.process_effects()
		# Iterate over pixels and draw them according to mapping
		for pos, color in self:
			x_coor = pos[0]
			y_coor = pos[1]
			pygame.draw.rect(self.surface, color, (x_coor * self.pixel_size, y_coor * self.pixel_size, self.pixel_size, self.pixel_size))

		# Flip vertically (pygame defines origin at the top left corner, we want to transform it to lower left corner)
		self.screen.blit(pygame.transform.flip(self.surface, False, True), (0, 0))
		pygame.display.flip()
		
		
	# def process_effects(self):
	# 	for effect, kwargs in self.effects:
	# 		effect.process(self, **kwargs)

