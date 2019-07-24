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
eff_rotate = eff.ModifyingEffectRotate(step_size=1, speed=1)
eff_rainbow = eff.ModifyingEffectRainbow(step_size=10, speed=1)

eff_rotate_2 = eff.ModifyingEffectRotate(step_size = -3, speed=1)

effect_cluster = eff.AppendingEffectPixelCluster(n=2
					,starting_position=0
					#, colors=[(255,0,0),(0,255,0),(0,0,255),(10,100,50),(80,10,100)]
					, colors = (255,0,0)
					, initial_pixels=pixels_array.copy()
					, separation = 1
					, modifying_effects=[eff_rotate, eff_rainbow])
effect_cluster_2 = eff.AppendingEffectPixelCluster(n=4, starting_position=100, colors = (255,0,0), initial_pixels=pixels_array.copy(), separation = 1, modifying_effects = [eff_rotate_2, eff_rainbow])

eff_rainbow_2 = eff.ModifyingEffectRainbow(step_size=1, speed=1)
effect_random_pixel = eff.AppendingEffectRandomPixels(initial_pixels = pixels_array.copy(), n=2, colors = (255,0,0), speed=0.3, modifying_effects = [eff_rainbow_2])



# Create collection of effects
collection = proc.EffectCollection(pixels, effects=[effect_cluster, effect_random_pixel, effect_cluster_2])

# Start show
collection.showtime(runtime=60)

collection.clear_effects()
collection.showtime(runtime=5)

