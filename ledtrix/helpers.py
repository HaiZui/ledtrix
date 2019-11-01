import collections
import colorsys
import numpy as np
from scipy import ndimage
from scipy.ndimage.interpolation import rotate

def int_to_rgb_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return (r, g, b)


def hsv_to_color(hue, saturation, value):
	t = colorsys.hsv_to_rgb(hue, saturation, value)
	return (int(t[0] * 255), int(t[1] * 255), int(t[2] * 255))

def darken_color(color, factor): # 0 is darkest, 1 is no change
	r,g,b=color
	return [int(r * factor), int(g * factor), int(b * factor)]

def brighten_color(color, factor): # 0 is brightest, 1 is no change
	r,g,b=color
	return [int(255 - (255 - r) * factor), int(255 - (255 - g) * factor), int(255 - (255 - b) * factor)]

def blend_colors(color1, color2, progress):
	b1 =  color1 & 255
	g1 = (color1 >> 8) & 255
	r1 = (color1 >> 16) & 255

	b2 =  color2 & 255
	g2 = (color2 >> 8) & 255
	r2 = (color2 >> 16) & 255

	inverted_progress = 1.0 - progress
	return (int(inverted_progress * r1 + progress * r2), int(inverted_progress * g1 + progress * g2), int(inverted_progress * b1 + progress * b2))
	

def color_rainbow_advance(color, step_size):
	# Unpack R, G and B channel values
	r, g, b = color
	assert(0<=r<=255 and 0<=g<=255 and 0<=b<=255), "Invalid color"
	# Process
	if r > 0 and b == 0:
		r = max(r-step_size, 0)
		g = min(g+step_size, 255)
	elif g > 0 and r == 0:
		g = max(g-step_size, 0)
		b = min(b+step_size, 255)
	elif b > 0 and g == 0:
		r = min(r+step_size, 255)
		b = max(b-step_size, 0)
	elif r == g == b == 0:
		pass
	else:
		b = max(b-step_size, 0)
	return (r, g, b)



# Sum of the min & max of (a, b, c)
def hilo(color):
	a = color[0]
	b = color[1]
	c = color[2]
	if c < b: 
		b, c = c, b
	if b < a: 
		a, b = b, a
	if c < b: 
		b, c = c, b	
	return a + c

def complement(color):
	r = color[0]
	g = color[1]
	b = color[2]
	k = hilo(color)
	return tuple(k - u for u in (r, g, b))


def add_image_arrays(array_1, array_2, pos=(0,0)):
	"""
	Add two matrices of different sizes in place, offset by xy coordinates
	Usage:
		- array_1: base matrix
		- array_2: add this matrix to array_1
		- pos: tuple (x,y) containing coordinates
	
	Arguments
	---------
	array_1 : numpy.array
		Base array
	array_2 : numpy.array
		Second array
	pos : tuple(int, int)
		xy coordination of the offset
	"""
	array_ret = array_1.copy()

	x, y = pos
	size_y_2, size_x_2, _ = array_2.shape
	size_y_1, size_x_1, _ = array_1.shape

	if x > size_x_1 or y > size_y_1:
		return array_1

	xmax, ymax = min(x + size_x_2, size_x_1), min(y + size_y_2, size_y_1)
	
	array_ret[y:ymax, x:xmax] += array_2[:size_y_1-y, :size_x_1-x]
	return array_ret


def rotate_image(img, angle, pivot):
    pivot = pivot.astype(np.int32)
    # double size of image while centering object
    pads = [[img.shape[0] - pivot[0], pivot[0]], [img.shape[1] - pivot[1], pivot[1]]]
    if len(img.shape) > 2:
        pads.append([0, 0])
    imgP = np.pad(img, pads, 'wrap')
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
                                                      reshape=False, prefilter=False, mode='nearest',order=4)
    rotated = imgP[pads[0][0]: -pads[0][1], pads[1][0]: -pads[1][1]] 
    return rotated


<<<<<<< HEAD
def effect_rainbow_color_advance(pixel_array, step_size):
    pixel_array_return = pixel_array
    for i in range(len(pixel_array)):
        for j in range(len(pixel_array[i])):
            if np.any(pixel_array[i][j] != [0,0,0]):
                pixel_array_return[i][j] = color_rainbow_advance(pixel_array[i][j],step_size=step_size)
    return pixel_array_return

def effect_complemetary_colors(pixel_array):
    pixel_array_return = pixel_array
    for i in range(len(pixel_array)):
        for j in range(len(pixel_array[i])):
            if np.any(pixel_array[i][j] != [0,0,0]):
                pixel_array_return[i][j] = complement(pixel_array[i][j])
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
=======
def reshape_image_array(array, size, origin=(0,0), center=False, mode='constant'):
	"""
	Reshapes image array keeping the scale and size of 
	the original image constant.

	Refills pixels if needed. 
	"""
	origin_x = origin[0]
	origin_y = origin[1]

	orig_size_x = len(array)
	orig_size_y = len(array[0])
	new_size_x = size[0]
	new_size_y = size[1]

	# Differences in lengths. 
	# These determine whether the image should be padded or cropped
	diff_x = new_size_x - orig_size_x - origin[0]
	diff_y = new_size_y - orig_size_y - origin[1]
	if origin == (0,0) and diff_x == 0 and diff_y == 0:
		# No need to do anything
		return array
	elif origin == (0,0) and diff_x <= 0 and diff_y <= 0:
		# Only crop
		return array[:orig_size_x+diff_x, :orig_size_y+diff_y]
	else:
		# Need to pad also
		cropped = array[max(-origin_x,0):new_size_x-origin_x,max(-origin_y,0):new_size_y-origin_y]
		return np.pad(cropped,((max(origin[0],0), max(diff_x,0)),(max(origin[1],0), max(diff_y,0)),(0,0)),mode=mode)[:new_size_x, :new_size_y]
>>>>>>> 5ac17eda27fdbbc2d4346e20f467d3f0cdc43b13
