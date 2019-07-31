import time
import numpy as np

import effects as eff
import process as proc

import neopixel
import board


# Initialize pixels
pixels = neopixel.NeoPixel(board.D18, 300, auto_write=False, brightness=0.5)
pixels_array = np.array(list(pixels))

# Create effects

# Create rotating and color changing 10 pixel cluster
eff_rotate = eff.ModifyingEffectRotate(step_size=1)
eff_rainbow = eff.ModifyingEffectRainbow(step_size=100)


effect_cluster = eff.AppendingEffectPixelCluster(n=5
					,starting_position=0
					, colors=[(255,0,0),(0,255,0),(0,0,255),(10,100,50),(80,10,100)]
					, initial_pixels=pixels_array
					, separation = 1
					,modifying_effects=[eff_rotate, eff_rainbow]) 

effect_random_pixel = eff.AppendingEffectRandomPixels(initial_pixels = pixels_array, n=1, colors = [(255,0,0)])


# Create collection of effects
collection = proc.EffectCollection(pixels, effects=[effect_cluster, effect_random_pixel], speeds=[2,1])

# Start show
collection.showtime(runtime=5)
collection.showtime(runtime=5)

