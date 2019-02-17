
class Sensor:
    '''Base class for all sensors'''

    def __init__(self):
        raise NotImplementedError

    def next_percept(self):
        '''Return the next percept'''
        raise NotImplementedError
