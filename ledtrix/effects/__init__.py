from ledtrix.triggers.triggers import TriggerChangeDirection, TriggerExponentialDecay, TriggerUpAndDown

class Effect:
    def __init__(self, triggers=None):
        self.triggers = triggers
        if self.triggers is None:
            self.triggers = []
        # triggered variables initialized
        self.direction = 1
        self.coefficient = 1

    def process_triggers(self):
        for trigger in self.triggers:
            if trigger.triggered is True:
                if isinstance(trigger, TriggerChangeDirection):
                    self.direction = trigger.process()
                elif isinstance(trigger, TriggerExponentialDecay):
                    self.coefficient = trigger.process()
                elif isinstance(trigger, TriggerUpAndDown):
                    self.coefficient = trigger.process()