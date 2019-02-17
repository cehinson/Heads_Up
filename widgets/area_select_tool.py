
from transparent_widget import TransparentWidget
from heads_up_widget import HeadsUpWidget

import sys
import json

from PySide2.QtWidgets import (
    QRubberBand,
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QCheckBox
)

from PySide2.QtCore import (
    Qt,
    QRect,
    QPoint,
    QSize,
    Signal,
    Slot,
)


class AreaSelectTool(QWidget):
    ''' Click on this to select area(s) of your screen '''

    def __init__(self):
        super(AreaSelectTool, self).__init__()
        self.layout = QVBoxLayout(self)
        # setup select screen widget
        self.ssw = AreaSelectWidget()
        self._make_connection(self.ssw)
        # keep track of area(s) selected
        self.selected_areas = []
        self.rects = []
        # setup button
        self.select_area_button = QPushButton("Select Area")
        self.select_area_button.clicked.connect(self.select_area)
        # checkbox to show selected areas
        self.show_selected_areas = QCheckBox("Show Selected Areas")
        self.show_selected_areas.setCheckState(Qt.CheckState.Checked)
        self.show_selected_areas.stateChanged.connect(
            self.toggle_selected_areas)
        # save the selected areas to a file
        self.save_button = QPushButton("Save and Exit")
        self.save_button.clicked.connect(self.save)
        # add to layout
        self.layout.addWidget(self.select_area_button)
        self.layout.addWidget(self.show_selected_areas)
        self.layout.addWidget(self.save_button)

    def select_area(self):
        self.hide()
        self.ssw.showMaximized()

    def toggle_selected_areas(self):
        for area in self.selected_areas:
            if not area.isHidden():
                area.hide()
            else:
                area.show()

    def save(self):
        with open('rects.json', 'w') as outfile:
            json.dump(self.rects, outfile)
        # FIXME this doesnt work
        self.close()

    @Slot(tuple)
    def area_selected(self, rect):
        self.ssw.hide()
        self.rects.append(rect)
        # show selected area
        self.addSelectedArea(rect)
        self.showSelectedArea(-1)  # show the most recent added
        self.show()

    def _make_connection(self, ssw_object):
        ssw_object.areaSelected.connect(self.area_selected)

    def showSelectedArea(self, index):
        self.selected_areas[index].show()

    def hideSelectedArea(self, index):
        self.selected_areas[index].hide()

    def addSelectedArea(self, rect):
        new_area = HeadsUpWidget(opacity=0.5)
        new_area.setStyleSheet('background-color: rgb(255, 0, 0)')
        x, y, w, h = rect
        new_area.setGeometry(x, y, w, h)
        self.selected_areas.append(new_area)

    def removeSelectedArea(self, index):
        self.selected_areas[index].close()
        del self.selected_areas[index]


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

    widget = AreaSelectTool()
    widget.show()

    sys.exit(app.exec_())
