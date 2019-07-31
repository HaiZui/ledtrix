import config


def create_screen():
	if config.virtual_hardware:
		from ledtrix.screen.virtualscreen import VirtualScreen
		return VirtualScreen(width=config.screen_w,height=config.screen_h)
	else:
		from ledtrix.screen.screen import Screen
		return Screen()