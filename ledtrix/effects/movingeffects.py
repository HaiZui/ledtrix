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
        self.angle += self.speed
        return rotate(pixel_array.astype(np.uint8), angle=self.angle, mode='nearest', reshape=True,order=2)
        # x0 = int(len(pixel_array) / 2)
        # y0 = int(len(pixel_array[0])/2)

        # return helpers.rotate_array(pixel_array, (x0,y0), self.angle)