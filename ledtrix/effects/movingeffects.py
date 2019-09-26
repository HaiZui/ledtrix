import numpy as np
from scipy.ndimage.interpolation import rotate
import ledtrix.helpers as helpers
from ledtrix.effects import Effect

class EffectRotate(Effect):
    def __init__(self, speed):
        # Use initial frame as a reference for rotating
        super().__init__(use_last_frame=False)
        self.speed = speed
        # Initialize angle
        self.angle = 0
        

    def process(self, pixel_array):
        # Set new angle
        self.angle += self.speed
        return rotate(pixel_array.astype(np.uint8), angle=self.angle, mode='nearest', reshape=True,order=2)

class EffectRoll(Effect):
    def __init__(self, axis, shift):
        # Use last frame as a reference
        super().__init__(use_last_frame=True)
        self.axis = axis
        self.shift = shift

    def process(self, pixel_array):
        return np.roll(pixel_array, axis=self.axis, shift=self.shift)
