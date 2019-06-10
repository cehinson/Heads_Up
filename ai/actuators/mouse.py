
from actuator import Actuator

import pyautogui
# move the mouse to the upper left corner of the screen to stop
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1  # pause one second between actions


class Rect:
    def __init__(self, coords: tuple):
        self.x, self.y, self.w, self.h = coords

    def __repr__(self):
        return('Rect[' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.w) + ', ' + str(self.h) + ']')

    def within(self, x, y):
        if x < self.x or x > self.x + self.w:
            raise pyautogui.FailSafeException
        if y < self.y or y > self.y + self.h:
            raise pyautogui.FailSafeException
        return True


class Mouse(Actuator):
    '''Controls mouse'''

    def __init__(self, boundary: Rect):
        super().__init__()
        # raise pyautogui.FailSafeException if not within boundary
        self.boundary = boundary

    @classmethod
    def from_file(self):
        raise NotImplementedError

    @Actuator.actions
    def moveTo(self, x, y, duration=0.0):
        # TODO add tweening
        if pyautogui.onScreen(x, y) and self.boundary.within(x, y):
            pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutCirc)

    @Actuator.actions
    def click(self, button='left', count=1):
        raise NotImplementedError

    @Actuator.actions
    def doubleClick(self):
        raise NotImplementedError

    @Actuator.actions
    def repeatedClick(self, interval, count, button='left'):
        pyautogui.click(clicks=count, interval=interval, button=button)


if __name__ == '__main__':
    # test the mouse actuator
    w, h = pyautogui.size()
    boundary = Rect((300, 300, w-300, h-300))
    print(boundary)
    myMouse = Mouse(boundary)
    myMouse.moveTo(400, 500, duration=0.5)
    # this should fail!
    myMouse.moveTo(200, 200)
