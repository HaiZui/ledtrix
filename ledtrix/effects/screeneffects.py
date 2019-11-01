import time
import numpy as np
from PIL import Image
from ledtrix.effects import Effect
from ledtrix.helpers import rotate_image, effect_complemetary_colors

class EffectChangeBrighness(Effect):
    def __init__(self, brightness, triggers=None):
        super(EffectChangeBrighness, self).__init__(triggers=triggers)
        self.brightness = brightness

    def initialize(self):
        self.coefficient = 1

    def process(self, screen):
        self.process_triggers()
        screen.brightness = self.coefficient * self.brightness

class EffectBlinkConstantly():
    def __init__(self, frequency):
        self.frequency=frequency
        # Initialize direction
        self.direction = 1
        self.last_update = time.time()
    
    def initialize(self):
        self.direction = 1
        self.last_update = time.time()

    def process(self, screen):
        time_now = time.time()
        elapsed_time = time_now - self.last_update
        self.last_update = time_now
        # Deduct new brightness
        if self.direction < 0:
            phase = np.pi / 2
        else:
            phase = -np.pi / 2
        elapsed_time_scaled = elapsed_time/self.frequency*(np.pi*2)

        loc = np.arcsin(2*screen.brightness-1) - phase
        if loc < 0:
            loc = np.abs(loc)

        new_brightness = (np.sin(elapsed_time_scaled+loc+phase) + 1) / 2

        if (elapsed_time_scaled+loc > np.pi):
            if self.direction < 0:
                self.direction = 1
            elif self.direction > 0:
                self.direction = -1 
        screen.brightness = new_brightness
    
    def trigger(self, screen):
        # Not triggered
        pass

    
class EffectComplementaryColor():
    def __init__(self, constant_color=True):
        self.constant_color = constant_color

    def initialize(self):
        pass

    def process(self, screen):
        screen.pixel = effect_complemetary_colors(screen.pixel)
        
        

    
class EffectRotate(Effect):
    def __init__(self, speed, triggers=None):
        super(EffectRotate, self).__init__(triggers=triggers)
        self.speed = speed
        # Initialize angle
        self.angle = 0

    def initialize(self):
        # Initialize angle
        self.angle = 0

    def process(self, screen):
        # Check triggers
        self.process_triggers()
        # Set new angle
        pixel_array = screen.canvas.pixel 
        self.angle += self.direction * self.speed
        # center pivot
        x, y, _ = pixel_array.shape
        pivot_x = int(x/2)
        pivot_y = int(y/2)
        rotated = rotate_image(pixel_array, self.angle, np.array([pivot_x,pivot_y]))
        # Debug
        # Image.fromarray(rotated.astype(np.uint8)).save('{}.png'.format(self.angle))
        screen.pixel = rotated

# class EffectChangeHue:
#     def __init__(self,)
    

