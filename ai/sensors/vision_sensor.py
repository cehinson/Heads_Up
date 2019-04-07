
from sensor import Sensor

import pyautogui


# TODO randomly writing this idea here:
'''
When an environment changes by x% :
    - take another screenshot
    - evalutate the reward given prev action
    - etc
'''


class VisionSensor(Sensor):
    '''Input from a region of the screen'''

    def __init__(self, rect):
        super().__init__()
        self.rect = rect

    def next_percept(self):
        # TODO benchmark this
        return pyautogui.screenshot(region=self.rect)


if __name__ == '__main__':
    vs = VisionSensor((0, 0, 300, 400))
    im = vs.next_percept()
    im.save('test.png')
    im.show()
