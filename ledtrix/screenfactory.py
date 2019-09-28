import config


def create_screen(brightness=1, effects=[]):
	if config.virtual_hardware:
		from ledtrix.screen.virtualscreen import VirtualScreen
		return VirtualScreen(width=config.screen_w,height=config.screen_h,brightness=brightness, effects=effects)
	else:
		from ledtrix.screen.screen import Screen
		return Screen(width=config.screen_w,height=config.screen_h, effects=effects)
