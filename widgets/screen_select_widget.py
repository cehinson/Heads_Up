
from transparent_widget import TransparentWidget

import sys

from PySide2.QtGui import (
    QPalette,
    QBrush,
    QColor
)

from PySide2.QtWidgets import (
    QRubberBand,
    QApplication
)

from PySide2.QtCore import (
    Qt,
    QRect,
    QPoint,
    QSize
)


class ScreenSelectWidget(TransparentWidget):
    '''A fully transparent widget used for selecting areas of a screen'''

    def __init__(self, width, height):
        super().__init__(opacity=0.50)
        self.resize(width, height)
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
        print("mousePressEvent")
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent")
        if not self.origin.isNull():
            self.rubberband.setGeometry(
                QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent")
        if event.button() == Qt.LeftButton:
            self.x = self.rubberband.x()
            self.y = self.rubberband.y()
            self.w = self.rubberband.width()
            self.h = self.rubberband.height()
            print(self.getCoords())

    def getCoords(self):
        return (self.x, self.y, self.w, self.h)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    widget = ScreenSelectWidget()
    widget.resize(size.width(), size.height())
    widget.show()

    sys.exit(app.exec_())
