
import pyautogui


# TODO randomly writing this idea here:
'''
When an environment changes by x% :
    - take another screenshot
    - evalutate the reward given prev action
    - etc
'''


class Camera:
    '''Input from a region of the screen'''

    def __init__(self, rect: tuple):
        super().__init__()
        self.rect = rect

    def next_frame(self):
        # TODO benchmark this
        # TODO make this async
        return pyautogui.screenshot(region=self.rect)


if __name__ == '__main__':
    vs = Camera((0, 0, 300, 400))
    im = vs.next_frame()
    im.save('test.png')
    im.show()
