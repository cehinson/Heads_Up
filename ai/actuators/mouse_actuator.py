
from actuators.actuator import Actuator

import pyautogui
# move the mouse to the upper left corner of the screen to stop
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1  # pause one second between actions


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def within(self, x, y):
        if x < self.x or x > self.x + self.w:
            return False
        if y < self.y or y > self.y + self.h:
            return False
        return True


class MouseActuator(Actuator):
    '''Controls mouse'''

    def __init__(self, boundary: Rectangle):
        # raise pyautogui.FailSafeException if not within boundary
        self.boundary = boundary

    @classmethod
    def from_file(self):
        raise NotImplementedError

    def moveTo(self, x, y, duration=0.0):
        # TODO add tweening
        if pyautogui.onScreen(x, y) and self.boundary.within(x, y):
            pyautogui.moveTo(x, y, duration=duration)

    def click(self, button='left', count=1):
        raise NotImplementedError

    def doubleClick(self):
        raise NotImplementedError

    def repeatedClick(self, interval, count, button='left'):
        pyautogui.click(clicks=count, interval=interval, button=button)


if __name__ == '__main__':
    # test the mouse actuator
    w, h = pyautogui.size()
    boundary = Rectangle(300, 300, w-300, h-300)
    test = MouseActuator(boundary)
