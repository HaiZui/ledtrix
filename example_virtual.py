import sys
import time
import numpy as np

from PIL import Image, ImageFile, ImageDraw

import ledtrix.screen.virtualcanvas as vc
import ledtrix.screen.abstractscreen as absc
import ledtrix.screen.shapes as s
from ledtrix.images import get_image_array


from ledtrix.effects.coloreffects import EffectColorTransformation, EffectRainbowTransformation
from ledtrix.effects.screeneffects import EffectRoll, EffectBlinkConstantly, EffectDiffusion
from ledtrix.triggers.triggers import TriggerChangeDirection, TriggerExponentialDecay, TriggerUpAndDown


import pygame

in_file_base = 'examples/gallery/2/mega_man_close.png'
image_base = get_image_array(in_file_base)

in_file_2 = 'examples/gallery/b.png'
image_2 = get_image_array(in_file_2)

# Virtual canvas starts a pygame window
canvas = vc.VirtualCanvas()

# Add screen
shape_1 = s.ScreenShapeRectangle(15,31, parallel_rows=False)

screen_effects_1 = [
			#(EffectRotate(speed=1, pivot=[15,15]),{})
			(EffectRoll( shift=(1,1)),{})
			,(EffectBlinkConstantly(frequency=1.5),{})
				]

screen_effects_2 = [
			#(EffectRotate(speed=1, pivot=[15,15]),{})
			(EffectRoll(shift=(-1,1)),{})
            ,(EffectDiffusion(speed=1),{})
			#,(EffectBlinkConstantly(frequency=2),{})
            	]

screen_1 = absc.AbstractScreen(canvas=canvas, shape=shape_1, brightness=1, effects=screen_effects_1)

# Add second screen
shape_2 = s.ScreenShapeRectangle(30,31, origin=(13,0), parallel_rows=False)
screen_2 = absc.AbstractScreen(canvas=canvas, shape=shape_2, brightness=0.5, effects=screen_effects_2)

canvas.set_pixels(np.array(image_base), overwrite=True)
# # Add secondary image
canvas.set_pixels(np.array(image_2), overwrite=False, pos=(0,0), opacity=0.2)
canvas.set_pixels(np.array(image_2), overwrite=False, pos=(10,0), opacity=0.4)
canvas.set_pixels(np.array(image_2), overwrite=False, pos=(20,0), opacity=1)

i = 1
start_time = time.time()
while True:
    if i % 100 == 0:
        time_elapsed = time.time() - start_time
        print(time_elapsed / i, ' per update')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit(), sys.exit()
    canvas.update()
    i += 1