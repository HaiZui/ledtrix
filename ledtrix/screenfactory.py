import config
from ledtrix.screen.canvas import Canvas
from ledtrix.screen.shapes import ScreenShapeRectangle

def create_canvas(width, height):
	return Canvas(width, height)

def create_screen(canvas=None, shape=None, brightness=1, effects=[]):
	if canvas is None:
		canvas = create_canvas(width=config.screen_w, height=config.screen_h)
	if shape is None:
		shape = ScreenShapeRectangle(canvas.width,canvas.height,0,0)
	if config.virtual_hardware:
		from ledtrix.screen.virtualscreen import VirtualScreen
		return VirtualScreen(canvas=canvas, shape=shape, brightness=brightness, effects=effects)
	else:
		from ledtrix.screen.screen import Screen
		return Screen(canvas=canvas, width=config.screen_w, height=config.screen_h, effects=effects)
