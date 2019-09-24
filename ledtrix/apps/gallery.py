
import os
from os import listdir
from ledtrix.apps import Module
import ledtrix.images as images
import pygame
import configparser
import time
from PIL import Image
from ledtrix.effects.coloreffects import EffectColorTransformation
from ledtrix.effects.movingeffects import EffectRotate

class Gallery(Module):
	def __init__(self, screen, filepath):
		super(Gallery, self).__init__(screen)

		print("Initializing Gallery")
		if filepath[:-1] != '/':
			filepath = filepath + '/'
		
		self.filepath = filepath
		self.screen = screen
        
		self.filenames = self.load_filenames(filepath)
		
		self.pos = 0
		self.load_image()
		self.screen.pixel = self.frames[0]
		self.screen.initial_pixel = self.frames[0]
		self.screen.update()
		self.interval = self.load_interval() 
		self.tick_interval = self.load_tick_interval()
		self.effects = [(EffectRotate(speed=10.),{})]

		self.start_time = time.time()
		
		self.start()

	def next_image(self):
		print("Gallery.next_image")
		self.pos = (self.pos + 1) % len(self.filenames)
		self.load_image()
		self.screen.pixel = self.frames[0]
		self.screen.initial_pixel = self.frames[0]
		self.screen.update() 

	def load_filenames(self, location):
		print("Gallery.load_filenames")
		if location[:1] != '/':
			location = location + '/'
		
		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")
		
		filenames = [location + f for f in listdir(location) if not f.endswith(".ini")]
		filenames.sort()
		
		if len(filenames) == 0:
			raise Exception("No bitmaps found in " + location)

		return filenames
	
	def load_image(self):
		print("Gallery.load_image")
		self.frames = []
		pixel_array = images.get_image_array(self.filenames[self.pos])
		self.frames.append(pixel_array)
	
	def load_interval(self):
		cfg = configparser.ConfigParser()
		cfg.read(self.filepath + 'config.ini')
		return cfg.getint('gallery', 'hold')
		
	def load_tick_interval(self):
		cfg = configparser.ConfigParser()
		cfg.read(self.filepath + 'config.ini')
		return cfg.getfloat('gallery', 'tick_interval')

	def tick(self):
		self.process_effects()
		self.screen.update() 
		time.sleep(self.tick_interval)
		if time.time() > self.start_time + self.interval:
			self.next_image()
			self.start_time = time.time()
		#time.sleep(self.interval)
		
	def on_start(self):
		print('Starting ' + self.filepath)

	def play_once(self):
		print("gallery.play_once")
		for frame in self.frames:
			self.screen.pixel = frame
			self.screen.update()
			time.sleep(self.interval)