
from actuators.actuator import Actuator

from functools import partial
import pyautogui
import yaml

# TODO pyautogui.press for attack keys, KeyDown and KeyUp for movement

class KeyboardActuator(Actuator):
    '''Controls keyboard'''

    def __init__(self, keys):
        for key in keys:
            if key not in pyautogui.KEYBOARD_KEYS:
                raise "Invalid Key"
        self.keys = keys
        self.actions = [partial(pyautogui.press, key) for key in keys]

    def to_file(self, filename):
        with open(filename, 'w') as outfile:
            yaml.dump(self.keys, outfile, default_flow_style=False)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as infile:
            keys = keys = yaml.load(infile)
            actuator = cls(keys)
            return actuator


if __name__ == '__main__':

    test_actuator = KeyboardActuator(['w', 'a', 's', 'd'])
    test_actuator.to_file('keyfile.yaml')
    test_actuator_2 = KeyboardActuator.from_file('keyfile.yaml')
    print(test_actuator_2.keys)
