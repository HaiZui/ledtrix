import numpy as np
import random
import process as proc

def random_color():
    list_rgb = range(1,256)
    r = random.choice(list_rgb)
    g = random.choice(list_rgb)
    b = 255 * 2 - r - g
    return (r, g, b)


# Effects
class ModifyingEffect:
        def __init__(self):
                self.name = 'ModifyingEffect'
		
class AppendingEffect:
        def __init__(self):
                self.name = 'AppendingEffect'

class ModifyingEffectRotate:
	def __init__(self, step_size):
		self.step_size = step_size

	def advance(self, pixels):
		pixels_new = np.roll(pixels, shift=self.step_size, axis=0)
		return pixels_new

#class ModifyingEffectFlicker:
#	def __init__(self, )

def color_fade_rainbow(color, step_size):
	# Unpack R, G and B channel values
	r, g, b = color
	assert(0<=r<=255 and 0<=g<=255 and 0<=b<=255), "Invalid color"
	# Process
	if r > 0 and b == 0:
		r = max(r+step_size, 0)
		g = min(g-step_size, 255)
	elif g > 0 and r == 0:
		g = max(g-step_size, 0)
		b = min(b+step_size, 255)
	elif b > 0 and g == 0:
		r = min(r+step_size, 255)
		b = max(b-step_size, 0)
	else:
		b = min(b+step_size, 255)
	return (r, g, b)

class ModifyingEffectRainbow:
	def __init__(self, step_size):
		self.step_size = step_size

	def advance(self, pixels):
		pixels_new = np.array([(0,0,0)]*len(pixels))
		for pixel in range(len(pixels)):
			if np.any(pixel != (0,0,0)) == True:
				pixels_new[pixel] = color_fade_rainbow(pixel, self.step_size)		
		return pixels_new

class AppendingEffectPixelCluster:
	def __init__(self, starting_position, initial_pixels, n, colors=None, separation=1, modifying_effects=[]):
		self.n = n
		if isinstance(colors, list) and len(color) == n:
			self.colors = colors
		elif isinstance(colors, list) and len(colors) != n:
			print("Length of colors has to match with number of pixels!")
		elif isinstance(colors, tuple):
			self.colors = [colors] * n
		else:
			# Do not set colors for now. Choose random colors at each update.
			self.colors = [None] * n

		self.separation = separation
		self.type = AppendingEffect()
		self.modifying_effects = modifying_effects
		# Initial state
		self.pixels = self._create_initial_pixels(initial_pixels)

		
	def _create_initial_pixels(self, pixels):
		i = 0
		for pixel_position in [(i*self.separation)%(len(pixels)-1) for i in range(self.n)]:
			pixels[pixel_position] = self.colors[i] or random_color()
			i+=1 
		return pixels
	
	def advance(self):
		for modifying_effect in self.modifying_effects:
			self.pixels = modifying_effect.advance(self.pixels)

	

class AppendingEffectRandomPixels:
	def __init__(self, initial_pixels, n, colors=None, modifying_effects=[]):
		self.n = n
		if isinstance(colors, list) and len(color) == n:
			self.colors = colors
		elif isinstance(colors, list) and len(colors) != n:
			print("Length of colors has to match with number of pixels!")
		elif isinstance(colors, tuple):
			self.colors = [colors] * n
		else:
			# Do not set colors for now. Choose random colors at each update.
			self.colors = [None] * n

		self.type = AppendingEffect()
		# Initial state
		self.state = initial_pixels

	def pixels(self, step, pixels_list):
		# Initialize pixels with original size
		pixels_out = np.array([(0,0,0)] * len(pixels_list))
		# Process pixels
		for i in range(self.n):
			random_i = random.choice(range(len(pixels_list)))
			color = self.colors[i] or proc.random_color()
			pixels_out[random_i] = color
		return pixels_out

