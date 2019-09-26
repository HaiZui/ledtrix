import numpy as np
from scipy import ndimage
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
        #return rotate(pixel_array.astype(np.uint8), angle=self.angle, mode='constant', reshape=True,order=4,prefilter=True,cval=100)
        return rotate_image(pixel_array, self.angle, np.array([15,5])) 
       

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

    return imgP[pads[0][0]: -pads[0][1], pads[1][0]: -pads[1][1]] 

class EffectRoll(Effect):
    def __init__(self, axis, shift):
        # Use last frame as a reference
        super().__init__(use_last_frame=True)
        self.axis = axis
        self.shift = shift

    def process(self, pixel_array):
        return np.roll(pixel_array, axis=self.axis, shift=self.shift)
