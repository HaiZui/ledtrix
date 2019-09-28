import collections
import colorsys
import numpy as np
from scipy.ndimage import rotate

def Color(r, g, b):
	return r * 65536 + g * 256 + b

RGBColor = collections.namedtuple('RGBColor', 'r g b')

def int_to_rgb_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return (r, g, b)

Point = collections.namedtuple('Point', 'x y')

def hsv_to_color(hue, saturation, value):
	t = colorsys.hsv_to_rgb(hue, saturation, value)
	return Color(int(t[0] * 255), int(t[1] * 255), int(t[2] * 255))

def rgb_to_int(c):
	return Color(c.r, c.g, c.b)

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
	return Color(int(inverted_progress * r1 + progress * r2), int(inverted_progress * g1 + progress * g2), int(inverted_progress * b1 + progress * b2))
	

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



def rotate_array(image, xy, angle):
    im_rot = rotate(image,angle) 
    org_center = (np.array(image.shape[:2][::-1])-1)/2.
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    org = xy-org_center
    a = np.deg2rad(angle)
    new = np.array([org[0]*np.cos(a) + org[1]*np.sin(a),
            -org[0]*np.sin(a) + org[1]*np.cos(a) ])
    return im_rot, new+rot_center