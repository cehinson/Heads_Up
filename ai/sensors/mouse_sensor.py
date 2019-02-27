
from sensor import Sensor
from collections import deque
from pynput import mouse


class MouseSensor(Sensor):
    '''Monitor mouse events'''

    def __init__(self):
        super().__init__()
        self.events = deque()

    def next_percept(self):
        return self.events.pop()
