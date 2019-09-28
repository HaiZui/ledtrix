import time
import numpy as np

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
        
        return screen