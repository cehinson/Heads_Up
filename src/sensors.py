
# Keyboard and Mouse Listeners
from pynput import mouse, keyboard
from collections import deque

# Camera
import multiprocessing
from multiprocessing import Queue, Process
import os
import sys
import numpy
from PIL import Image
import mss
import pytesseract


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

    # TODO add method to stop

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

    # TODO add method to stop

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
    # TODO maybe list_of_funcs could be either a list of partials or an actionlist
    def __init__(self, screen, out_dir='screenshots'):

        # ex: screen = {"top": 40, "left": 0, "width": 800, "height": 640}
        self.screen = screen
        self.out_dir = out_dir

        # TODO this need to be updated in the area slect tool
        self.rects_to_segment = []

        self._running = False
        # it seems like maybe each function should have their own queues
        self.queue = Queue()
        self.processes = []
        self.funcs_to_run = [self.grab, self.save]

    def start(self):
        assert(len(self.funcs_to_run) < multiprocessing.cpu_count())
        self._running = True
        for func in self.funcs_to_run:
            # TODO add args
            process = Process(target=func)
            process.start()
            self.processes.append(process)

    def terminate(self):
        self._running = False
        for process in self.processes:
            process.terminate()

    def grab(self):
        '''
        Grab a portion of the screen
        '''
        # TODO add a way to limit the fps...
        print('grabbing screen')
        while self._running:
            with mss.mss() as sct:
                img = sct.grab(self.screen)
                img = numpy.array(sct.grab(self.screen))
                img = Image.fromarray(img)
                # TODO should i move segmentation somewhere else?
                for rect in self.rects_to_segment:
                    # FIXME the coords are wrong because of how QT does the screen size
                    coords = [rect.x(), rect.y(), rect.x()+rect.width(), rect.y()+rect.height()]
                    sub_img = img.crop(box=coords)
                    self.queue.put(sub_img)
        self.queue.put(None)

    def ocr(self):
        print('running ocr')
        while True:
            img = self.queue.get()

            if img is None:
                break

            # for rect in self.rects_to_segment:
            #     sub_img = img[rect.x():rect.width(), rect.y():rect.height(), :]
            print(pytesseract.image_to_string(img))
            sys.stdout.flush()  # FIXME this does not seem to work

    def save(self):
        ''' Save the images in the queue '''
        print('saving')
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)

        # out file naming
        number = 0
        output = self.out_dir + "/file_{}.png"

        while True:  # "there are screenshots":
            img = self.queue.get()
            if img is None:
                break

            img.save(output.format(number))
            number += 1
