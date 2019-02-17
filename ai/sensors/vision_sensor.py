
from sensor import Sensor

import pyautogui


class VisionSensor(Sensor):
    '''Input from a region of the screen'''

    def __init__(self, rect):
        self.rect = rect

    def next_percept(self):
        return pyautogui.screenshot(region=self.rect)


if __name__ == '__main__':
    vs = VisionSensor((0, 0, 300, 400))
    im = vs.next_percept()
    im.save('test.png')
    im.show()
