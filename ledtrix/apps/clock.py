import collections
import random
import time
import datetime
import os
import math
import numpy as np
from PIL import ImageDraw, ImageFont, Image
from ledtrix.helpers import *
from ledtrix.apps import Module

class Clock(Module):
	def __init__(self, screen):
		super(Clock, self).__init__(screen)
		
	
	def draw_time(self, color, colon = True):
		height = self.screen.height
		width = self.screen.width

		now = datetime.datetime.now()
		hour = "{:02d}".format(now.hour)
		minute = "{:02d}".format(now.minute)
		second = "{:02d}".format(now.second)
		current_time = hour + ':' + minute + ':' + second
		print(current_time)
		img = Image.new('RGB', (width, height), color = (0, 0, 0))
		d = ImageDraw.Draw(img)
		font = ImageFont.truetype("fonts/TooSimple.ttf", 4)
		d.text((0,0), current_time, fill=color, font=font)
		pixel_values = list(img.getdata())
		pixel_values = np.array(pixel_values).reshape((height, width, 3))
		self.screen.pixel = pixel_values
			

	def draw(self, colon = True):
		self.screen.clear()
		self.draw_time((255, 255, 0), colon)
		self.screen.update()
	
	def tick(self):
		self.draw(False)
		time.sleep(0.5)
		self.draw(True)
		time.sleep(0.5)
