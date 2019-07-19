import pyautogui
from collections import deque
from pynput import mouse, keyboard


class MouseListener:
    '''Monitor mouse events'''

    def __init__(self):
        super().__init__()
        self.events = deque()
        # Collect events until released
        with mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        ) as listener:
            listener.join()

    def on_move(self, x, y):
        self.events.append((x, y))
        print('Pointer moved to {0}'.format((x, y)))

    def on_click(self, x, y, button, pressed):
        self.events.append((x, y, button, pressed))
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(self, x, y, dx, dy):
        self.events.append((x, y, dx, dy))
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))


class KeypressListener:
    '''Monitor and record key presses'''

    def __init__(self):
        super().__init__()
        self.events = deque()
        # Collect events until released
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()

    def next_percept(self):
        return self.events.pop()

    def on_press(self, key):
        self.events.append(key)
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(self, key):
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False


class Camera:
    '''Input from a region of the screen'''

    def __init__(self, rect: tuple):
        super().__init__()
        self.rect = rect

    def next_frame(self):
        # TODO benchmark this
        # TODO make this async
        # img = pyscreenshot.grab(childprocess=False)
        # img = numpy.array(img)
        return pyautogui.screenshot(region=self.rect)
