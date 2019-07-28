import images


class AppendingEffectRectangle:
	def __init__(self, canvas_size, xy, w, h, fill_color, outline_color=None, modifying_effects=[]):
		self.canvas_size
        self.xy = xy
        self.w = w
        self.h = h
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.modifying_effects = modifying_effects

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

# class AppendingEffectImage:
#     def __init__
