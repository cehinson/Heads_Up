
from transparent_widget import TransparentWidget

import sys

from PySide2.QtGui import (
    QPalette,
    QBrush,
    QColor
)

from PySide2.QtWidgets import (
    QRubberBand,
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout
)

from PySide2.QtCore import (
    Qt,
    QRect,
    QPoint,
    QSize,
    QObject,
    Signal,
    Slot,
)


class SelectScreenButton(QWidget):
    def __init__(self):
        super(SelectScreenButton, self).__init__()
        # setup select screen widget
        self.ssw = ScreenSelectWidget()
        self.make_connection(self.ssw)
        # setup button
        self.select_area_button = QPushButton("Select Area")
        self.select_area_button.clicked.connect(self.select_area)
        # add to layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.select_area_button)

    def select_area(self):
        self.hide()
        self.ssw.showMaximized()

    @Slot(tuple)
    def area_selected(self, rect):
        self.ssw.hide()
        print("Area selected")
        print(rect)
        self.show()

    def make_connection(self, ssw_object):
        ssw_object.areaSelected.connect(self.area_selected)


class ScreenSelectWidget(TransparentWidget):
    '''A fully transparent widget used for selecting areas of a screen'''

    # add a signal
    areaSelected = Signal(tuple)

    def __init__(self):
        super().__init__(opacity=0.50)
        # select area
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        # FIXME set the color
        # self.pal = QPalette()
        # self.pal.setColor(QPalette.Highlight, Qt.red)
        # self.pal.setBrush(QPalette.Highlight, QBrush(Qt.red))
        # self.rubberband.setPalette(self.pal)

        self.origin = QPoint()
        # selected areas coords
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberband.setGeometry(
                QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.x = self.rubberband.x()
            self.y = self.rubberband.y()
            self.w = self.rubberband.width()
            self.h = self.rubberband.height()
            self.areaSelected.emit(self.getCoords())
            self.rubberband.hide()

    def getCoords(self):
        return (self.x, self.y, self.w, self.h)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = SelectScreenButton()
    widget.show()

    sys.exit(app.exec_())
