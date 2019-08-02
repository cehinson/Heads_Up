
from utils import clear_screen, timeblock, timethis

# Keyboard and Mouse Listeners
from pynput import mouse, keyboard
from collections import deque

# Camera
from multiprocessing import Process
import os
import numpy
import cv2
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
    def __init__(self, screen, pixel_ratio, out_dir='camera'):
        # save images to an output folder for logging / debugging
        self.out_dir = out_dir
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)
        self.number = 0

        # ex: screen = {"top": 40, "left": 0, "width": 800, "height": 640}
        self.screen = screen
        # deal with high-dpi screens
        self.pixel_ratio = pixel_ratio

        # NOTE updated in the area slect tool
        self.rects_to_segment = []

        # make opencv run fast
        if not cv2.useOptimized():
            cv2.setUseOptimized(True)
            assert(cv2.useOptimized() is True)

        # ---------- Things for Multiprocessing ----------

        self._running = False
        self._process = None

    def start(self):
        self._running = True
        # TODO add args
        process = Process(target=self.grab)
        process.start()
        self._process = process

    def terminate(self):
        # TODO can terminate a specific process
        self._running = False
        self._process.join()  # I think i need to do this to guarantee no zombies
        self._process.terminate()

    def grab(self):
        ''' Grab a portion of the screen '''
        # TODO add a way to limit the fps...
        while self._running:
            with mss.mss() as sct:
                # take screenshot of entire screen
                img = numpy.array(sct.grab(self.screen))
                sub_imgs = []
                # FIXME what if no sub images...
                # segment all user labeled areas of the screen
                # and group into subgroups for processing
                with timeblock('segment {} '.format(len(self.rects_to_segment))):
                    for rect in self.rects_to_segment:
                        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
                        # account for the difference in pixel coordinates in QT and numpy
                        x = int(round(x * self.pixel_ratio))
                        y = int(round(y * self.pixel_ratio))
                        w = int(round(w * self.pixel_ratio))
                        h = int(round(h * self.pixel_ratio))
                        # NOTE opencv indexes with y first
                        sub_img = img[y:y+h, x:x+w].copy()
                        sub_imgs.append(sub_img)

                # process the sub images...
                with timeblock('ocr {} '.format(len(sub_imgs))):
                    for img in sub_imgs:
                        text = self.ocr(img)
                        print(text)

    def ocr(self, img):
        ''' Optical Character Recognition '''
        # convert to gray and threshold
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # perform ocr
        text = pytesseract.image_to_string(img) + ""
        return text

    def save(self, img):
        ''' Save the images in the queue '''
        # TODO save based on which subimage they belong to

        # out file naming
        output = self.out_dir + "/file_{}.png"

        img = Image.fromarray(img)
        img.save(output.format(self.number))
        self.number += 1
