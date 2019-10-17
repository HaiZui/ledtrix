import numpy as np
import time

class TriggerChangeDirection:
    def __init__(self):
        self.triggered = False
        # initialize
        self.direction = 1
    
    def process(self):
        self.triggered = False
        return self.direction

    def trigger(self):
        self.triggered = True
        self.direction = -1 * self.direction
        


class TriggerExponentialDecay:
    def __init__(self, lifetime, minimum_brightness = 0, initial_value = 0):
        self.lifetime = lifetime
        self.minimum_brightness = minimum_brightness
        self.initial_value = initial_value
        
        self.triggered = False
        # initialize
        self.last_update = time.time()

    def process(self):
        time_now = time.time()
        # Elapsed time in milliseconds
        elapsed_time = (time_now - self.last_update) * 1000
        self.value = max(np.exp(-elapsed_time/self.lifetime), self.minimum_brightness)
        if self.value < 0.05:
            self.triggered = False
        return self.value

    def trigger(self):
        # Trigger and initialize
        self.triggered = True
        self.last_update = time.time()

class TriggerUpAndDown:
    def __init__(self, lifetime, max_multiplier=1.5):
        self.lifetime = lifetime
        self.max_multiplier = max_multiplier

        # Initialize
        self.multiplier = 1
        self.triggered = False
        self.last_update = time.time()

    def process(self):
        time_now = time.time()
        elapsed_time = time_now - self.last_update
        if elapsed_time < self.lifetime and self.triggered is True:
            elapsed_time_scaled = (self.lifetime - elapsed_time) / self.lifetime * np.pi
            self.multiplier = 1 + np.sin(elapsed_time_scaled) * (self.max_multiplier - 1)
        else:
            self.multiplier = 1
            self.triggered = False

        return self.multiplier

    def trigger(self):
        self.triggered = True
        self.last_update = time.time()