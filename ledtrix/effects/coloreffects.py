import numpy as np
from ledtrix.effects import Effect
import ledtrix.helpers as helpers



class EffectColorTransformation(Effect):
    """
    Advances pixel array color 
    """
    def __init__(self, angle):
        # Use last frame as a reference
        super().__init__()
        self.angle = angle

    def initialize(self):
        pass
    
    def process(self, pixel_array):
        theta = self.angle / 180 * np.pi
        im_normed = helpers.do_normalise(pixel_array)
        im_rotated = np.einsum("ijk,lk->ijl", im_normed, helpers.rotation_matrix(theta))
        im2 = helpers.undo_normalise(im_rotated)
        return im2


class EffectRainbowTransformation(Effect):
    """
    Advances pixel array colors with rainbow transformation
    """
    def __init__(self, step_size):
        # Use last frame as a reference
        super().__init__()
        self.step_size = step_size

    def initialize(self):
        pass

    def process(self, pixel_array):
        return  helpers.effect_rainbow_color_advance(pixel_array, self.step_size)


