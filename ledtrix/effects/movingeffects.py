import numpy as np
from scipy import ndimage
from scipy.ndimage.interpolation import rotate
import ledtrix.helpers as helpers
from ledtrix.effects import Effect

from PIL import Image

class EffectRotate(Effect):
    def __init__(self, speed):
        # Use initial frame as a reference for rotating
        super().__init__()
        self.speed = speed
        # Initialize angle
        self.angle = 0

    def initialize(self):
        # Initialize angle
        self.angle = 0

    def process(self, pixel_array):
        # Set new angle
        self.angle += self.speed
        # center pivot
        x, y, _ = pixel_array.shape
        pivot_x = int(x/2)
        pivot_y = int(y/2)
        rotated = helpers.rotate_image(pixel_array, self.angle, np.array([pivot_x,pivot_y]))
        # Debug
        # Image.fromarray(rotated.astype(np.uint8)).save('{}.png'.format(self.angle))
        return rotated
       


class EffectRoll(Effect):
    def __init__(self, axis, shift):
        # Use last frame as a reference
        super().__init__()
        self.axis = axis
        self.shift = shift

    def initialize(self):
        pass

    def process(self, pixel_array):
        return np.roll(pixel_array, axis=self.axis, shift=self.shift)


class EffectDiffusion(Effect):
    def __init__(self, speed):
        # Use last frame as a reference
        super().__init__()
        self.speed = speed

    def initialize(self):
        pass

    def process(self, pixel_array):
        axis = (0,1,2)
        shift_x = int(np.random.normal(scale=self.speed,size=1))
        shift_y = int(np.random.normal(scale=self.speed,size=1))
        shift = (shift_x,shift_y,0)
        return np.roll(pixel_array, axis=axis, shift=shift)