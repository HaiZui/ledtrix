import numpy as np
from scipy import ndimage
from scipy.ndimage.interpolation import rotate
import ledtrix.helpers as helpers
from ledtrix.effects import Effect

from PIL import Image

class EffectRotate(Effect):
    def __init__(self, speed):
        # Use initial frame as a reference for rotating
        super().__init__(use_last_frame=False)
        self.speed = speed
        # Initialize angle
        self.angle = 0

    def initialize(self):
        # Initialize angle
        self.angle = 0

    def process(self, pixel_array):
        # Set new angle
        self.angle += self.speed
        #return rotate(pixel_array.astype(np.uint8), angle=self.angle, mode='constant', reshape=True,order=4,prefilter=True,cval=100)
        # center pivot
        x, y, _ = pixel_array.shape
        pivot_x = int(x/2)
        pivot_y = int(y/2)
        rotated = rotate_image(pixel_array, self.angle, np.array([pivot_x,pivot_y]))
        # Debug
        # Image.fromarray(rotated.astype(np.uint8)).save('{}.png'.format(self.angle))
        return rotated
       

def rotate_image(img, angle, pivot):
    pivot = pivot.astype(np.int32)
    # double size of image while centering object
    pads = [[img.shape[0] - pivot[0], pivot[0]], [img.shape[1] - pivot[1], pivot[1]]]
    if len(img.shape) > 2:
        pads.append([0, 0])
    imgP = np.pad(img, pads, 'constant')
    # reduce size of matrix to rotate around the object
    if len(img.shape) > 2:
        total_y = np.sum(imgP.any(axis=(0, 2))) * 30.
        total_x = np.sum(imgP.any(axis=(1, 2))) * 30.
    else:
        total_y = np.sum(imgP.any(axis=0)) * 30.
        total_x = np.sum(imgP.any(axis=1)) * 30.
    cropy = int((imgP.shape[0] - total_y)/2)
    cropx = int((imgP.shape[1] - total_x)/2)
    imgP[cropy:-cropy, cropx:-cropx] = ndimage.rotate(imgP[cropy:-cropy, cropx:-cropx], angle,
                                                      reshape=False, prefilter=False, mode='constant',order=4)
    rotated = imgP[pads[0][0]: -pads[0][1], pads[1][0]: -pads[1][1]] 
    return rotated

class EffectRoll(Effect):
    def __init__(self, axis, shift):
        # Use last frame as a reference
        super().__init__(use_last_frame=True)
        self.axis = axis
        self.shift = shift

    def initialize(self):
        pass

    def process(self, pixel_array):
        return np.roll(pixel_array, axis=self.axis, shift=self.shift)


class EffectDiffusion(Effect):
    def __init__(self, speed):
        # Use last frame as a reference
        super().__init__(use_last_frame=True)
        self.speed = speed

    def initialize(self):
        pass

    def process(self, pixel_array):
        axis = (0,1,2)
        shift_x = int(np.random.normal(scale=self.speed,size=1))
        shift_y = int(np.random.normal(scale=self.speed,size=1))
        shift = (shift_x,shift_y,0)
        return np.roll(pixel_array, axis=axis, shift=shift)