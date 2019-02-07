
class Agent():
    '''
    Something that percieves and acts in an environment.
    Base class for all other agents.
    '''

    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def next_action(self):
        raise NotImplementedError
