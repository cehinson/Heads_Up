
from actuator import Actuator
from actuator import ActionList

import pyautogui
import yaml

# TODO pyautogui.press for attack keys, KeyDown and KeyUp for movement
# TODO is there a difference between KeyDown + KeyUp and press?


class KeyboardActuator(Actuator):
    '''Controls keyboard'''
    actions = ActionList()

    def __init__(self, keys, allow_combos=False):
        super().__init__()
        for key in keys:
            if key not in pyautogui.KEYBOARD_KEYS:
                raise "Invalid Key"
        self.keys = keys
        self._is_down = dict((key, False) for key in keys)
        self.allow_combos = allow_combos
        # TODO maybe add pyautogui.press as well
        # self.actions = keys
        # self.actions = [partial(pyautogui.keyDown, key) for key in keys] + \
        #     [partial(pyautogui.keyUp, key) for key in keys]

    def to_file(self, filename):
        # TODO save which type of keypress is called
        with open(filename, 'w') as outfile:
            yaml.dump(self.keys, outfile, default_flow_style=False)

    @actions.register
    def from_file(cls, filename):
        with open(filename, 'r') as infile:
            keys = keys = yaml.load(infile)
            actuator = cls(keys)
            return actuator

    @actions.register
    def press(self, key):
        pyautogui.press(key)

    def is_down(self, key):
        return self._is_down[key]

    @actions.register
    def down(self, key):
        # FIXME cant press an already down key
        if not self.allow_combos:
            for k in self.keys:
                if self._is_down[k]:
                    self.up(k)
        pyautogui.keyDown(key)

    @actions.register
    def up(self, key):
        # FIXME cant lift an already up key
        pyautogui.keyUp(key)


if __name__ == '__main__':

    test_actuator = KeyboardActuator(['w', 'a', 's', 'd'])
    # test_actuator.to_file('keyfile.yaml')
    # test_actuator_2 = KeyboardActuator.from_file('keyfile.yaml')
    # print(test_actuator_2.keys)
    print(KeyboardActuator.actions._actions)
    for action in KeyboardActuator.actions:
        print(action)
