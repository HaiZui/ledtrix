import sys
import numpy as np

from PIL import Image, ImageFile, ImageDraw

import ledtrix.screen.canvas as c
import ledtrix.screen.virtualscreen as vs
import ledtrix.screen.shapes as s
from ledtrix.images import get_image_array

import pygame

in_file_base = 'examples/gallery/2/mega_man_close.png'
image_base = get_image_array(in_file_base)

in_file_2 = 'examples/gallery/b.png'
image_2 = get_image_array(in_file_2)

canvas = c.Canvas(50,32)

canvas.set_pixels(np.array(image_base), overwrite=False)
# Add secondary image
canvas.set_pixels(np.array(image_2), overwrite=False, pos=(0,0), opacity=0.2)
canvas.set_pixels(np.array(image_2), overwrite=False, pos=(10,0), opacity=0.4)
canvas.set_pixels(np.array(image_2), overwrite=False, pos=(20,0), opacity=1)

#print(canvas.pixel)
shape = s.ScreenShapeRectangle(14,31, parallel_rows=False)
screen = vs.VirtualScreen(canvas=canvas, shape=shape, brightness=1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit(), sys.exit()
        else:
            screen.update()