import time

from agents.random_agent import Random_Agent
from actuators.actuator import Actuator

test_actuator = Actuator(("North", "South", "East", "West"))
agent = Random_Agent(None, test_actuator)

input("Press any key to continue...")
while True:
    action = agent.next_action()
    print(action)
    time.sleep(2)
