
from actuators.actuator import Actuator

import pyautogui
# move the mouse to the upper left corner of the screen to stop
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1  # pause one second between actions


class MouseActuator(Actuator):
    '''Controls mouse'''

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_file(self):
        raise NotImplementedError
