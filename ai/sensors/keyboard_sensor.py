
from sensor import Sensor
from collections import deque
from pynput import keyboard


class KeyboardSensor(Sensor):
    '''Monitor key presses '''

    def __init__(self):
        super().__init__()
        self.events = deque()


    def next_percept(self):
        return self.events.pop()
