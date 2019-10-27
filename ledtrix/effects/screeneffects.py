import time
import numpy as np
from PIL import Image
from ledtrix.effects import Effect
from ledtrix.effects.coloreffects import effect_complemetary_colors
from ledtrix.helpers import rotate_image, reshape_image_array

class EffectOverlay(Effect):
    def __init__(self, screen_other, alpha=0, triggers=None):
        super(EffectOverlay, self).__init__(triggers=triggers)
        self.screen_other = screen_other
        self.alpha = alpha

    def initialize(self):
        pass

    def process(self, screen):
        self.process_triggers()
        alpha = self.coefficient * self.alpha
        cropped_other = reshape_image_array(self.screen_other.pixel, size=(screen.width, screen.height), origin=(0,0))
        screen.pixel = (1-alpha) * screen.pixel + alpha * cropped_other


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
        

    
class EffectRotate(Effect):
    def __init__(self, speed, pivot=None, triggers=None):
        super(EffectRotate, self).__init__(triggers=triggers)
        self.speed = speed
        self.pivot = pivot
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
        if self.pivot is None:
            pivot_x = int(x/2)
            pivot_y = int(y/2)
            pivot = [pivot_x, pivot_y]
        else:
            pivot = self.pivot
        rotated = rotate_image(pixel_array, self.angle, np.array(pivot))
        # Debug
        # Image.fromarray(rotated.astype(np.uint8)).save('{}.png'.format(self.angle))
        screen.pixel = rotated
    

class EffectRoll(Effect):
    def __init__(self, axis, shift):
        # Use last frame as a reference
        super().__init__()
        self.axis = axis
        self.shift = shift
        # Initialize
        self.shift_x = 0
        self.shift_y = 0
        self.shift_z = 0

    def initialize(self):
        self.shift_x = 0
        self.shift_y = 0
        self.shift_z = 0

    def process(self, screen):
        self.shift_x += self.shift[0]
        self.shift_y += self.shift[1]
        self.shift_z += self.shift[2]
        screen.pixel = np.roll(screen.pixel, axis=self.axis, shift=[self.shift_x, self.shift_y, self.shift_z])
