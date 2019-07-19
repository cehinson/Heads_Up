# miscellaneous functions to help widgets go here
import numpy
from PySide2.QtWidgets import QApplication


def qimage_to_numpy_array(q_image):
    ptr = q_image.constBits()
    arr = numpy.array(ptr).reshape(q_image.width(), q_image.height(), 4)  # Copies the data
    return arr


def scale_pixels(x, y, w, h):
    # actual screen dimentions (opencv will use this)
    # FIXME this only works when no external screen is connected...
    actual_width = 2880
    actual_height = 1800
    # screen size in QT
    qt_size = QApplication.desktop().screenGeometry()

    x = int(x / actual_width * qt_size.width())
    w = int(w / actual_width * qt_size.width())
    y = int(y / actual_height * qt_size.height())
    h = int(h / actual_height * qt_size.height())

    return x, y, w, h