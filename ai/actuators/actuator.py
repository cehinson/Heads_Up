
from action import ActionList


class Actuator:
    '''Base class for all actuators'''
    # all actions available to all actuators
    actions = ActionList()

    def __init__(self):
        pass
