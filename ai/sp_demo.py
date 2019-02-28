'''
Demo for StreetPyghter
'''

import time

from agents.random_agent import RandomAgent
from actuators.keyboard_actuator import KeyboardActuator

keyboard = KeyboardActuator(['w', 'a', 's', 'd', 'b', 'n', 'm'])
agent = RandomAgent(None, keyboard)

input("Press any key to continue...")
while True:
    action = agent.next_action()
    action()
    time.sleep(1)
