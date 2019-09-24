import numpy as np
from ledtrix.helpers import color_rainbow_advance



def effect_rainbow_color_advance(pixel_array, step_size):
    pixel_array_return = pixel_array
    for i in range(len(pixel_array)):
        for j in range(len(pixel_array)):
            pixel_array_return[i][j] = color_rainbow_advance(pixel_array[i][j],step_size=step_size)
    return pixel_array_return


def do_normalise(im):
    return -np.log(1/((1 + im)/257) - 1)
 
def undo_normalise(im):
    return (1 + 1/(np.exp(-im) + 1) * 257).astype("uint8")

def rotation_matrix(theta):
    """
    3D rotation matrix around the X-axis by angle theta
    """
    return np.c_[
        [1,0,0],
        [0,np.cos(theta),-np.sin(theta)],
        [0,np.sin(theta),np.cos(theta)]
    ]

class EffectColorTransformation:
    def __init__(self, angle):
        self.angle = angle

    def process(self, pixel_array):
        theta = self.angle / 180 * np.pi
        im_normed = do_normalise(pixel_array)
        im_rotated = np.einsum("ijk,lk->ijl", im_normed, rotation_matrix(theta))
        im2 = undo_normalise(im_rotated)
        return im2