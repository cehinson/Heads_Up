
from collections import deque
from pynput import mouse


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


if __name__ == '__main__':
    mysensor = MouseListener()
    while True:
        pass
