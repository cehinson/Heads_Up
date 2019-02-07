
import pyautogui
# move the mouse to the upper left corner of the screen to stop
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1  # pause one second between actions


class Actuator():
    '''
    Base class for all actuators
    '''

    def __init__(self, actions):
        self.actions = actions


class keyboard(Actuator):
    '''
    Plays games which only require keyboard input
    '''

    def __init__(self, actions):
        super().__init__(actions)
