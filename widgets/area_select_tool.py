
from transparent_widget import TransparentWidget
from heads_up_widget import HeadsUpWidget

# from matplotlib import cm
import random

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
    ''' Select areas of your screen '''

    def __init__(self):
        super(AreaSelectTool, self).__init__()
        self.layout = QVBoxLayout(self)
        # setup widget for selecting areas of the screen
        self.area_edit_widget = AreaEditWidget()
        self._make_connection(self.area_edit_widget)
        # keep track of area(s) selected
        self.selected_areas = []
        self.rects = []
        # button to add / remove a specific area
        self.edit_area_button = QPushButton("Add / Remove Areas")
        self.edit_area_button.clicked.connect(self.edit_area)
        # checkbox to show selected areas
        self.show_selected_areas = QCheckBox("Show Selected Areas")
        self.show_selected_areas.setCheckState(Qt.CheckState.Checked)
        self.show_selected_areas.stateChanged.connect(
            self.toggle_selected_areas
        )
        # save the selected areas to a file
        self.save_button = QPushButton("Save and Exit")
        self.save_button.clicked.connect(self.save)
        # reset selected areas
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        # add all ui elements to layout
        self.layout.addWidget(self.edit_area_button)
        self.layout.addWidget(self.show_selected_areas)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.save_button)

    def _make_connection(self, ssw_object):
        # connect the buttons to AreaEditWidgets signals
        ssw_object.areaSelected.connect(self.area_selected)
        ssw_object.areaRemoved.connect(self.area_removed)

    def edit_area(self):
        self.hide()
        self.area_edit_widget.showMaximized()

    @Slot(QRect)
    def area_selected(self, rect):
        self.area_edit_widget.hide()
        # add the selected area
        self.rects.append(rect)
        new_area = HeadsUpWidget(opacity=0.5)
        new_area.setGeometry(rect)
        # randomly assign a color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color_str = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        new_area.setStyleSheet('background-color: ' + color_str)

        self.selected_areas.append(new_area)
        self.selected_areas[-1].show()  # show the most recent added

        self.show()

    @Slot(QPoint)
    def area_removed(self, pos):
        self.area_edit_widget.hide()
        # remove the area that was clicked on
        for i, x in enumerate(zip(self.rects, self.selected_areas)):
            r, a = x  # TODO can I do this in only one line?
            if r.contains(pos):
                a.close()
                del self.selected_areas[i]
                del self.rects[i]

        self.show()

    def toggle_selected_areas(self):
        for area in self.selected_areas:
            if not area.isHidden():
                area.hide()
            else:
                area.show()

    def reset(self):
        '''remove all selected areas'''
        for area in self.selected_areas:
            area.close()

        del self.selected_areas
        del self.rects
        self.selected_areas = []
        self.rects = []

    def save(self):
        '''Save the selected areas to a json file and quit the app'''
        outdict = {i: [r.x(), r.y(), r.width(), r.height()] for i, r in enumerate(self.rects)}
        with open('rects.json', 'w') as outfile:
            json.dump(outdict, outfile)
        app.exit()


class AreaEditWidget(TransparentWidget):

    # add a signal that emits the area selected
    areaSelected = Signal(QRect)
    areaRemoved = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(opacity=0.25)
        # QLabel.__init__(self, parent)
        # select area
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        # coords of mouse click
        self.origin = QPoint()
        # account for the dock / menu bar
        self.x_offset = QApplication.desktop().availableGeometry().x()
        self.y_offset = QApplication.desktop().availableGeometry().y()

    def mousePressEvent(self, event):
        # left click starts the rubber band
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()
        # right click on a selected area to remove it
        if event.button() == Qt.RightButton:
            print(event.pos())
            # FIXME not sure if this offset is needed...
            offset = QPoint(self.x_offset, self.y_offset)
            pos = event.pos() + offset
            self.areaRemoved.emit(pos)

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
            print(coords)
            self.areaSelected.emit(coords)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = AreaSelectTool()
    widget.show()

    sys.exit(app.exec_())
