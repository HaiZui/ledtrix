import pygame
import collections
from ledtrix.screen.abstractscreen import AbstractScreen
from PIL import Image

class VirtualScreen(AbstractScreen):
	def __init__(self, width = 30, height = 20):		
		super(VirtualScreen, self).__init__(width, height)
		self.pixel_size = 30
		
		pygame.display.init()
		self.screen = pygame.display.set_mode([width * self.pixel_size, height * self.pixel_size], 0)
		self.surface = pygame.Surface(self.screen.get_size())	
				
	def update(self):
		for x in range(len(self.pixel)):
			for y in range(len(self.pixel[x])):
				if x <= self.width and y <= self.height:
					x_coor = x
					y_coor = self.height - y
					pygame.draw.rect(self.surface, tuple(self.pixel[x][y]), (x_coor * self.pixel_size, (y_coor - 1) * self.pixel_size, self.pixel_size, self.pixel_size))

		self.screen.blit(self.surface, (0, 0))
		pygame.display.flip()
		pygame.display.update()
