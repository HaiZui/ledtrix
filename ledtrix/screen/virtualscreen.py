import pygame
import collections
from ledtrix.screen.abstractscreen import AbstractScreen, ScreenShapeRectangle
from ledtrix.helpers import darken_color
from PIL import Image

class VirtualScreen(AbstractScreen):
	def __init__(self, canvas=None, width = 30, height = 20, brightness=1, effects=[]):		
		print(effects)
		super(VirtualScreen, self).__init__(canvas=canvas, shape=ScreenShapeRectangle(width, height), brightness=brightness, effects=effects)
		self.width = width
		self.height = height
		self.pixel_size = 30
		print(self.effects)
		pygame.display.init()
		self.screen = pygame.display.set_mode([width * self.pixel_size, height * self.pixel_size], 0)
		self.surface = pygame.Surface(self.screen.get_size())	
				
	def update(self):
		self._crop_canvas()
		self.process_effects()
		for x in range(len(self.pixel)):
			for y in range(len(self.pixel[x])):
				if x <= self.width and y <= self.height:
					x_coor = x
					y_coor = self.height - y
					color = darken_color(tuple(self.pixel[x][y]),factor=self.brightness)
					pygame.draw.rect(self.surface, color, (x_coor * self.pixel_size, (y_coor - 1) * self.pixel_size, self.pixel_size, self.pixel_size))

		self.screen.blit(self.surface, (0, 0))
		pygame.display.flip()
		pygame.display.update()
		
		
	def process_effects(self):
		for effect, kwargs in self.effects:
			effect.process(self, **kwargs)

