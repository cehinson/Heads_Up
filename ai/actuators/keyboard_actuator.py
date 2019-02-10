
from actuators.actuator import Actuator

import pyautogui


class keyboardActuator(Actuator):
    '''Controls keyboard'''

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_file(cls):
        raise NotImplementedError
