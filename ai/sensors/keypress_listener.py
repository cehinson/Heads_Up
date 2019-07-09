
from collections import deque
from pynput import keyboard


class KeypressListener:
    '''Monitor and record key presses'''

    def __init__(self):
        super().__init__()
        self.presses = deque()
        # Collect events until released
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()

    def next_percept(self):
        return self.events.pop()

    def on_press(self, key):
        self.presses.append(key)
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(self, key):
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False


if __name__ == '__main__':
    mysensor = KeypressListener()
    while True:
        pass
