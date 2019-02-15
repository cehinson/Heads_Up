
from transparent_widget import TransparentWidget
from heads_up_widget import HeadsUpWidget

import sys

from PySide2.QtWidgets import (
    QRubberBand,
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel
)

from PySide2.QtCore import (
    Qt,
    QRect,
    QPoint,
    QSize,
    Signal,
    Slot,
)


class AreaSelectButton(QWidget):
    ''' Click on this to select area(s) of your screen '''
    def __init__(self):
        super(AreaSelectButton, self).__init__()
        self.layout = QVBoxLayout(self)
        # setup select screen widget
        self.ssw = AreaSelectWidget()
        self.make_connection(self.ssw)
        # keep track of area(s) selected
        # TODO select multiple areas
        self.selected_area = HeadsUpWidget(opacity=0.5)
        self.selected_area.setStyleSheet('background-color: rgb(255, 0, 0)')
        # setup button
        self.select_area_button = QPushButton("Select Area")
        self.select_area_button.clicked.connect(self.select_area)
        # setup text to display coordinates selected
        # self.selected_area_text = QLabel()
        # add to layout
        self.layout.addWidget(self.select_area_button)

    def select_area(self):
        self.hide()
        self.ssw.showMaximized()

    @Slot(tuple)
    def area_selected(self, rect):
        self.ssw.hide()
        print("Area selected")
        print(rect)
        # show selected area
        x, y, w, h = rect
        self.selected_area.setGeometry(x, y, w, h)
        self.selected_area.show()
        # self.layout.addWidget(self.selected_area_text)
        # self.selected_area_text.setText(str(rect))
        self.show()

    def make_connection(self, ssw_object):
        ssw_object.areaSelected.connect(self.area_selected)


class AreaSelectWidget(TransparentWidget):
    '''A fully transparent widget used for selecting areas of a screen'''

    # add a signal that emits the area selected
    areaSelected = Signal(tuple)

    def __init__(self):
        super().__init__(opacity=0.25)
        # select area
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        # coords of mouse click
        self.origin = QPoint()
        # selected area rect
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

    widget = AreaSelectButton()
    widget.show()

    sys.exit(app.exec_())
