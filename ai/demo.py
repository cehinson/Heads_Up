
import time
from functools import partial

from agents.random_agent import RandomAgent
from actuators.actuator import Actuator

test_actuator = Actuator([partial(print, "North"),
                          partial(print, "South"),
                          partial(print, "East"),
                          partial(print, "West")])

agent = RandomAgent(None, test_actuator)

input("Press any key to continue...")
while True:
    action = agent.next_action()
    action()
    time.sleep(1)
