
from actuator import Actuator
from action import ActionList

import pyautogui
import yaml

# TODO pyautogui.press for attack keys, KeyDown and KeyUp for movement
# TODO is there a difference between KeyDown + KeyUp and press?


key_action = ActionList()


class KeyboardActuator(Actuator):
    '''Controls keyboard'''

    def __init__(self, keys, allow_combos=False):
        super().__init__()
        for key in keys:
            if key not in pyautogui.KEYBOARD_KEYS:
                raise "Invalid Key"
        self.keys = keys
        self._is_down = dict((key, False) for key in keys)
        self.allow_combos = allow_combos
        # TODO maybe add pyautogui.press as well

    def to_file(self, filename):
        # TODO save which type of keypress is called
        with open(filename, 'w') as outfile:
            yaml.dump(self.keys, outfile, default_flow_style=False)

    def from_file(cls, filename):
        with open(filename, 'r') as infile:
            keys = keys = yaml.load(infile)
            actuator = cls(keys)
            return actuator

    def press(self, key):
        pyautogui.press(key)

    def is_down(self, key):
        return self._is_down[key]

    def down(self, key):
        # FIXME cant press an already down key
        if not self.allow_combos:
            for k in self.keys:
                if self._is_down[k]:
                    self.up(k)
        pyautogui.keyDown(key)

    def up(self, key):
        # FIXME cant lift an already up key
        pyautogui.keyUp(key)


if __name__ == '__main__':

    test_actuator = KeyboardActuator(['w', 'a', 's', 'd'])
