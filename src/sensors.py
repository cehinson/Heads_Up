import mss
from mss.tools import to_png
from pynput import mouse, keyboard

from collections import deque
import os
import numpy
import time


class MouseListener:
    '''Monitor mouse events'''

    def __init__(self):
        super().__init__()
        self.events = deque()

    def start(self):
        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        listener.start()

    # TODO add method to start

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

    def start(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()

    # TODO add method to start

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
    # TODO calculate the fps
    def __init__(self, rect):
        self.rect = rect

        self.out_dir = 'screenshots'
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)

        self._running = False

    def start(self):
        print(self._running)
        self._running = True

    def terminate(self):
        print(self._running)
        self._running = False

    def grab(self, out_queue):
        '''
        Grab a portion of the screen
        rect = {"top": 40, "left": 0, "width": 800, "height": 640}
        '''
        while self._running:
            with mss.mss() as sct:
                # img = numpy.array(sct.grab(self.rect))
                img = sct.grab(self.rect)
                out_queue.put(img)
        out_queue.put(None)

    def segment(self, in_queue):
        ''' Perform segmentation on images '''
        raise NotImplementedError

    def save(self, in_queue):
        ''' Save the images in the queue '''
        number = 0
        output = self.out_dir + "/file_{}.png"

        while True:  # "there are screenshots":
            img = in_queue.get()
            if img is None:
                break

            to_png(img.rgb, img.size, output=output.format(number))
            number += 1
