import numpy as np
from scipy.ndimage.interpolation import rotate
import ledtrix.helpers as helpers


class EffectRotate:
    def __init__(self, angle):
        self.angle = angle

    def process(self, pixel_array):
        return rotate(pixel_array.astype(np.uint8), angle=self.angle, mode='nearest', reshape=True,order=2)
        # x0 = int(len(pixel_array) / 2)
        # y0 = int(len(pixel_array[0])/2)

        # return helpers.rotate_array(pixel_array, (x0,y0), self.angle)