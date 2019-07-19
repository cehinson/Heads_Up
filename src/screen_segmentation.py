
import random
from widgets.transparent_widget import HeadsUpWidget
from widgets.utils import scale_pixels, qimage_to_numpy_array
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QPixmap
import cv2
import numpy
import sys


import pyscreenshot



app = QApplication(sys.argv)

# screen = app.primaryScreen()
# img = screen.grabWindow(app.desktop().winId()).toImage()
# img = qimage_to_numpy_array(img)

# FIXME
# do not spawn a child process, this seems to conflict with QT's threading
img = pyscreenshot.grab(childprocess=False)
img = numpy.array(img)

# swap the channels...
img = cv2.cvtColor(img, cv2.cv2.COLOR_RGBA2GRAY)
# cv2.imshow('im', img)
# cv2.waitKey()
# find contours
im = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# open and close
kernel = numpy.ones((3, 3), numpy.uint8)
# im = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
# im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)

# cv2.imshow('im', im)
# cv2.waitKey()
contours, _ = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

areas = []


for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # x, y, w, h = scale_pixels(x, y, w, h)
    if w * h >= 1000 and w * h <= 5000:
        new_area = HeadsUpWidget(opacity=0.75)
        new_area.setGeometry(x, y, w, h)
        # randomly assign a color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color_str = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        new_area.setStyleSheet('background-color: ' + color_str)
        new_area.show()
        areas.append(new_area)
    # draw a green rectangle to visualize the bounding rect
    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

print(len(contours))
# cv2.drawContours(im, contours, -1, (255, 255, 0), 1)

# cv2.imshow("contours", img)

cv2.waitKey()
sys.exit(app.exec_())
