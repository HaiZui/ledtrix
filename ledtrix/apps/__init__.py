from _thread import start_new_thread
import time

class Module(object):
	def __init__(self, screen, effects=[]):
		self.screen = screen
		self.effects = effects
		self.running = False

	def tick(self):
		raise Exception("All modules must implement tick")

	def run(self):
		while self.running:
			self.tick()

	def start(self):
		if self.running:
			return
		
		self.running = True
		start_new_thread(self.run, ())

		self.on_start()
 		
	def process_effects(self):
		for effect, kwargs in self.effects:
			if effect.use_last_frame == True:
				self.screen.pixel = effect.process(self.screen.pixel, **kwargs)
			elif effect.use_last_frame == False:
				self.screen.pixel = effect.process(self.screen.initial_pixel, **kwargs)

	def stop(self):
		self.running = False
		self.on_stop()
		time.sleep(1)

	def on_start(self):
		pass

	def on_stop(self):
		pass