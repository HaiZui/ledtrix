import config
from ledtrix.screen.canvas import Canvas

def create_canvas(width, height):
	return Canvas(width, height)

def create_screen(canvas=None, brightness=1, effects=[], abstract=False):
	if canvas is None:
		canvas = create_canvas(width=config.screen_w, height=config.screen_h)
	if abstract is True:
		from ledtrix.screen.abstractscreen import AbstractScreen, ScreenShapeRectangle
		return AbstractScreen(canvas=canvas, shape=ScreenShapeRectangle(canvas.width,canvas.height,0,0), brightness=brightness, effects=effects)
	if config.virtual_hardware:
		from ledtrix.screen.virtualscreen import VirtualScreen
		return VirtualScreen(canvas=canvas,width=config.screen_w,height=config.screen_h,brightness=brightness, effects=effects)
	else:
		from ledtrix.screen.screen import Screen
		return Screen(canvas=canvas, width=config.screen_w,height=config.screen_h, effects=effects)
