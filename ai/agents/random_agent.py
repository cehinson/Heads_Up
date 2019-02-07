
import random


class Random_Agent(Agent):
    '''Agent that moves randomly'''

    def __init__(self, sensors, actuators):
        super().__init__(sensors, actuators)
        self.actions = actuators.actions

    def next_action(self):
        return self.random_action()

    def random_action(self):
        return random.choice(self.actions)
