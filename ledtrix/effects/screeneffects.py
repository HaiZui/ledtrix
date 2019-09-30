import time
import numpy as np

class EffectExponentialFade():
    def __init__(self, lifetime):
        """
        half_life: float
            Half life of decay in milliseconds
        """
        self.lifetime = lifetime
        self.last_update = time.time()
        # Initialize brightness coefficient
        self.brightness_init = 1

    def process(self, screen):
        time_now = time.time()
        # Elapsed time in milliseconds
        elapsed_time = (time_now - self.last_update) * 1000
        screen.brightness = np.exp(-elapsed_time/self.lifetime)

    def trigger(self, screen):
        # Trigger and initialize
        self.last_update = time.time()

class EffectBlinkConstantly():
    def __init__(self, frequency):
        self.frequency=frequency
        # Initialize direction
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