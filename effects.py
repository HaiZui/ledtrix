# Use python 3.x
from time import sleep, time
import random
import argparse

import board
import neopixel



RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

def turn_off(pixels, index):
    pixels[index] = (0, 0, 0)

def turn_on(pixels, index, color):
    pixels[index] = color

def clear(pixels):
    pixels.fill((0,0,0))

def random_color():
    list_rgb = range(255)
    r = random.choice(list_rgb)
    g = random.choice(list_rgb)
    b = random.choice(list_rgb)
    return (r, g, b)


def advance_color(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)

    return (r, g, b)

def adjust_tail(tail):
    dimmed_tail = [tuple(int(tail[i][j] * 2**(-i)) for j in range(len(tail[i]))) for i in range(len(tail))]
    return dimmed_tail

def flash_random_pixel(pixels, time):
    random_pixel_index = random.choice(range(len(pixels)))
    pixels[random_pixel_index] = random_color()
    pixels.show()
    sleep(time)
    turn_off(pixels, random_pixel_index)
    return random_pixel_index

def flash_pixel(pixels, index, color, max_time=None, flash_time=0.1):
    if max_time is None:
        end_time = time() + 60
    else:
        end_time = time() + max_time

    while True:
        # Turn on
        pixels[index] = color
        pixels.show()
        sleep(flash_time)
        turn_off(pixels, index)
        pixels.show()
        sleep(flash_time)


# Main program
def wheel(tail_length):
    tail_positions = [(i+10*i)%255 for i in range(tail_length)]
    color_seqment = [advance_color(i) for i in tail_positions]

    #loop_i = 0
    try:
        loop_i = 0
        while True:
            for index in range(len(pixels)):
                    random_pixel_index = flash_random_pixel(pixels, 0.001)
                    clear(pixels)
                    color_seqment = adjust_tail([advance_color(i%255) for i in tail_positions])
                    print(color_seqment)
                    for tail_i in range(tail_length):
                        turn_on(pixels, index-tail_i, color_seqment[tail_i])

                    pixels.show()
                    sleep(0.001)
                    tail_positions = [i+2 for i in tail_positions]
                    loop_i += 1
            break
        print('Winner is number {}'.format(random_pixel_index))
        flash_pixel(pixels, random_pixel_index, RED, 0.3)
    except KeyboardInterrupt:
        clear(pixels)
        pixels.show()
        pass

    print('\nExiting')
    clear(pixels)
    pixels.show()



# New module
class EffectCollection:
	def __init__(self, pixels, effects=[], speeds=[]):
		self.pixels = pixels
		self.effects = effects
		
		if len(speeds) == len(effects):
			self.speeds = speeds
		else:
			self.speeds = [1 for i in range(len(effects))]
			
		# Initialize step
		self.step = 0
	

	def add_effect(self, effect, relative_speed=1, kwargs=None):
		self.effects.append((effect, kwargs))
		self.speeds.append(relative_speed)

	def calculate_pixels_at_step(self, step):
		self.clear()
		pixels = self.pixels
		for effect_i in range(len(self.effects)):
			step_cur = int(self.speeds[effect_i] * step)
			effect_cur, kwargs_cur = self.effects[effect_i]
			pixels_cur = effect_cur.func(step_cur, pixels, **kwargs_cur)
			if isinstance(effect_cur, ModifyingEffect):
				pixels = pixels_cur
			elif isinstance(effect_cur, AppendingEffect):
				pixels = self._combine_pixels(pixels_cur, pixels)
				
		return pixels

	def _combine_pixels(self, pixels, pixels_other):
		pixels_return = pixels
		for i in range(pixels.n):
			if pixels_other[i] == (0,0,0):
				pixels_return[i] = pixels[i]
			elif pixels[i] == (0,0,0):
				pixels_return[i] = pixels_other[i]
			else:
				pixels_return[i] = pixels[i]
		return pixels
			

	def jump_to_step(self, step):
		self.pixels = self.calculate_pixels_at_step(step)
	
	def calculate_pixels(self):
		pixels = self.calculate_pixels_at_step(self.step)
		return pixels
	
	def advance(self):
		self.step += 1
	
	def show(self):
		self.pixels.show()

	def clear(self):
		self.pixels.fill((0,0,0))

	def showtime(self):
		try:
			while True:
				print(self.pixels)
				self.calculate_pixels()
				self.show()
				self.advance()				

		except KeyboardInterrupt:
			self.clear()
			self.show()
			pass
			




# Effects
class ModifyingEffect:
	def __init__(self, func):
		self.func = func

class AppendingEffect:
	def __init__(self, func):
		self.func = func


def effect_turn_on_constant_pixel(step, pixels, pixel_index, color):
	#pixels_copy = pixels.copy()
	pixels[pixel_index] = color
	return pixels

