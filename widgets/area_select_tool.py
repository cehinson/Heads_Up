
from transparent_widget import TransparentWidget
from heads_up_widget import HeadsUpWidget

import sys
import json

from PySide2.QtWidgets import (
    QRubberBand,
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QCheckBox
)

from PySide2.QtCore import (
    Qt,
    QRect,
    QMargins,
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
        self.area_select_widget = AreaSelectWidget()
        self._make_connection(self.area_select_widget)
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
            self.toggle_selected_areas
        )
        # save the selected areas to a file
        self.save_button = QPushButton("Save and Exit")
        self.save_button.clicked.connect(self.save)
        # add to layout
        self.layout.addWidget(self.select_area_button)
        self.layout.addWidget(self.show_selected_areas)
        self.layout.addWidget(self.save_button)
        print(QApplication.desktop().screenGeometry())

    def select_area(self):
        self.hide()
        self.area_select_widget.showMaximized()

    def toggle_selected_areas(self):
        for area in self.selected_areas:
            if not area.isHidden():
                area.hide()
            else:
                area.show()

    def save(self):
        outdict = dict(enumerate(self.rects))
        with open('rects.json', 'w') as outfile:
            json.dump(outdict, outfile)
        app.exit()

    @Slot(tuple)
    def area_selected(self, rect):
        self.area_select_widget.hide()
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
        self.rects.append(rect)
        new_area = HeadsUpWidget(opacity=0.5)
        # TODO make different colors for easier identification
        new_area.setStyleSheet('background-color: rgb(255, 0, 0)')
        new_area.setGeometry(rect)
        self.selected_areas.append(new_area)

    def removeSelectedArea(self, index):
        del self.rects[index]
        self.selected_areas[index].close()
        del self.selected_areas[index]


class AreaSelectWidget(TransparentWidget):
    '''A fully transparent widget used for selecting areas of a screen'''

    # add a signal that emits the area selected
    areaSelected = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(opacity=0.25)
        # QLabel.__init__(self, parent)
        # select area
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        # coords of mouse click
        self.origin = QPoint()

        self.x_offset = QApplication.desktop().availableGeometry().x()
        self.y_offset = QApplication.desktop().availableGeometry().y()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberband.hide()
            area_selected = self.rubberband.geometry()
            coords = QRect(
                self.x_offset + area_selected.x(),
                self.y_offset + area_selected.y(),
                area_selected.width(),
                area_selected.height()
            )
            self.areaSelected.emit(coords)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = AreaSelectTool()
    widget.show()

    sys.exit(app.exec_())
