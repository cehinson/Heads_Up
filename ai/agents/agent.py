
class Agent:
    '''
    Base class for other agents
    '''

    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def next_action(self):
        raise NotImplementedError
