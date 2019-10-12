import time
import numpy as np
from ledtrix.effects.coloreffects import effect_complemetary_colors
from ledtrix.helpers import rotate_image

class EffectExponentialFade():
    def __init__(self, lifetime, minimum_brightness = 0):
        """
        half_life: float
            Half life of decay in milliseconds
        """
        self.lifetime = lifetime
        self.last_update = time.time()
        self.minimum_brightness = minimum_brightness

    def initialize(self):
        self.last_update = time.time()

    def process(self, screen):
        time_now = time.time()
        # Elapsed time in milliseconds
        elapsed_time = (time_now - self.last_update) * 1000
        screen.brightness = max(np.exp(-elapsed_time/self.lifetime), self.minimum_brightness)

    def trigger(self, screen):
        # Trigger and initialize
        self.last_update = time.time()

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
        pass

    
class EffectComplementaryColor():
    def __init__(self, constant_color=True):
        self.constant_color = constant_color
        # Initialize
        self.is_complement = 0

    def initialize(self):
        self.is_complement = 0

    def process(self, screen):
        if self.is_complement == 0:
            screen.pixel = effect_complemetary_colors(screen.pixel)
            if self.constant_color is True:
                self.is_complement = 1

    def trigger(self, screen):
        self.is_complement = 0
        

    
class EffectRotate():
    def __init__(self, speed):
        self.speed = speed
        # Initialize angle
        self.angle = 0

    def initialize(self):
        # Initialize angle
        self.angle = 0

    def process(self, screen):
        # Set new angle
        pixel_array = screen.pixel
        self.angle += self.speed
        #return rotate(pixel_array.astype(np.uint8), angle=self.angle, mode='constant', reshape=True,order=4,prefilter=True,cval=100)
        # center pivot
        x, y, _ = pixel_array.shape
        pivot_x = int(x/2)
        pivot_y = int(y/2)
        rotated = rotate_image(pixel_array, self.angle, np.array([pivot_x,pivot_y]))
        # Debug
        # Image.fromarray(rotated.astype(np.uint8)).save('{}.png'.format(self.angle))
        screen.pixel = rotated