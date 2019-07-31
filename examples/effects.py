import numpy as np
import random
import process as proc
import copy

def random_color():
    list_rgb = range(1,256)
    r = random.choice(list_rgb)
    g = random.choice(list_rgb)
    b = 255 * 2 - r - g
    return (r, g, b)

def effect_advance_step(step, speed):
	step_old = step
	step_new = step + speed
	is_updated = int(step_old) != int(step_new)
	return (step_new, is_updated)

# Effects
class ModifyingEffect:
        def __init__(self):
                self.name = 'ModifyingEffect'
		
class AppendingEffect:
        def __init__(self):
                self.name = 'AppendingEffect'

class ModifyingEffectRotate:
	def __init__(self, step_size, speed):
		self.step_size = step_size
		self.speed = speed
		# Initialize step
		self.step = 0

	def advance(self, pixels):
		step_new, is_updated = effect_advance_step(self.step, self.speed)
		print(step_new, is_updated)
		self.step = step_new

		if is_updated == True:
			pixels_new = np.roll(pixels, shift=self.step_size, axis=0)
			return pixels_new
		else:
			return pixels

	def clear(self):
		self.step = 0

#class ModifyingEffectFlicker:
#	def __init__(self, )

def color_fade_rainbow(color, step_size):
	# Unpack R, G and B channel values
	r, g, b = color
	assert(0<=r<=255 and 0<=g<=255 and 0<=b<=255), "Invalid color"
	# Process
	if r > 0 and b == 0:
		r = max(r-step_size, 0)
		g = min(g+step_size, 255)
	elif g > 0 and r == 0:
		g = max(g-step_size, 0)
		b = min(b+step_size, 255)
	elif b > 0 and g == 0:
		r = min(r+step_size, 255)
		b = max(b-step_size, 0)
	elif r == g == b == 0:
		pass
	else:
		b = min(b+step_size, 255)
	return (r, g, b)

class ModifyingEffectRainbow:
	def __init__(self, step_size, speed=1):
		self.step_size = step_size
		self.speed = speed
		# Initialize step
		self.step = 0

	def advance(self, pixels):
		step_new, is_updated = effect_advance_step(self.step, self.speed)
		self.step = step_new
		if is_updated == True:
			pixels_new = np.array([(0,0,0)]*len(pixels))
			for pixel in range(len(pixels)):
				if np.any(pixel != (0,0,0)) == True:
					pixels_new[pixel] = color_fade_rainbow(pixels[pixel], self.step_size)			
		else:
			pixels_new = pixels

		return pixels_new

	def clear(self):
		self.step = 0

class AppendingEffectPixelCluster:
	def __init__(self, starting_position, initial_pixels, n, colors=None, separation=1, modifying_effects=[]):
		self.n = n
		if isinstance(colors, list) and len(colors) == n:
			self.colors = colors
		elif isinstance(colors, list) and len(colors) != n:
			print("Length of colors has to match with number of pixels!")
		elif isinstance(colors, tuple):
			self.colors = [colors] * n
		else:
			# Do not set colors for now. Choose random colors at each update.
			self.colors = [None] * n

		self.separation = separation
		self.modifying_effects = modifying_effects
		# Initial state
		self.pixels = self._create_initial_pixels(initial_pixels)
		
	def _create_initial_pixels(self, pixels):
		i = 0
		pixels = copy.deepcopy(pixels)
		for pixel_position in [(i*self.separation)%(len(pixels)-1) for i in range(self.n)]:
			pixels[pixel_position] = self.colors[i] or random_color()
			i+=1 
		return pixels
	
	def advance(self):
		for modifying_effect in self.modifying_effects:
			self.pixels = modifying_effect.advance(self.pixels)

	def clear(self):
		self.pixels = np.array([(0,0,0)] * self.pixels)
		for effect in self.modifying_effects:
			effect.clear()
		self.pixels = self._create_initial_pixels(self.pixels)

class AppendingEffectRandomPixels:
	def __init__(self, initial_pixels, n, speed, colors=None, modifying_effects=[]):
		self.n = n
		self.speed = speed
		if isinstance(colors, list) and len(colors) == n:
			self.colors = colors
		elif isinstance(colors, list) and len(colors) != n:
			print("Length of colors has to match with number of pixels!")
		elif isinstance(colors, tuple):
			self.colors = [colors] * n
		else:
			# Do not set colors for now. Choose random colors at each update.
			self.colors = [None] * n

		# Initial state
		self.pixels = copy.deepcopy(initial_pixels)
		# Initialize step
		self.step = 0

		# Possible modifying effects (e.g. color fade)
		self.modifying_effects = modifying_effects

	def advance(self):
		step_new, is_updated = effect_advance_step(self.step, self.speed)	
		self.step = step_new
		if is_updated == True:
			# Initialize pixels with original size		
			pixels_out = np.array([(0,0,0)] * len(self.pixels))
			# Process pixels
			for i in range(self.n):
				random_i = random.choice(range(len(self.pixels)))
				color = self.colors[i] or random_color()
				pixels_out[random_i] = color
			print(pixels_out)
			self.pixels = pixels_out
		print(self.pixels)
		# Process modifications
		for modifying_effect in self.modifying_effects:
			self.pixels = modifying_effect.advance(self.pixels)
	
	def clear(self):
		self.step = 0
		self.pixels = np.array([(0,0,0)]*self.pixels)
		for effect in self.modifying_effects:
			effect.clear()
