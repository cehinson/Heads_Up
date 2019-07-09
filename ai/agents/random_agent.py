
from agents.agent import Agent

import random


class RandomAgent(Agent):

    def __init__(self, sensors, actuators):
        super().__init__(sensors, actuators)
        self.actions = actuators.actions

    def next_action(self):
        '''Choose next action randomly'''
        return random.choice(self.actions)
