
from transparent_widget import TransparentWidget, HeadsUpWidget

# from matplotlib import cm
import random

import sys
import json

from ai.sensors.mouse_listener import MouseListener

from PySide2.QtWidgets import (
    QRubberBand,
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QCheckBox,
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

    def __init__(self, screen_size):
        super(AreaSelectTool, self).__init__()
        # keep track of area(s) selected
        self.selected_areas = []
        # follow mouse movements
        # self.mouse_listener = MouseListener()

        # ---------- Setup GUI ----------

        self.screen_size = screen_size
        self.layout = QVBoxLayout(self)
        # setup widget for selecting areas of the screen
        self.area_edit_widget = AreaEditWidget()
        self._make_connection(self.area_edit_widget)
        # button to add / remove a specific area
        self.edit_area_button = QPushButton("Add / Remove Areas")
        self.edit_area_button.clicked.connect(self.edit_area)
        # checkbox to show / hide selected areas
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
        self.area_edit_widget.resize(
            self.screen_size.width(),
            self.screen_size.height()
        )
        self.area_edit_widget.show()

    @Slot(QRect)
    def area_selected(self, rect):
        self.area_edit_widget.hide()
        # add the selected area
        new_area = HeadsUpWidget(opacity=0.5)
        new_area.setGeometry(rect)
        # randomly assign a color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color_str = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        new_area.setStyleSheet('background-color: ' + color_str)

        new_area.show()
        # add the new area to the list
        self.selected_areas.append(new_area)

        self.show()

    @Slot(QPoint)
    def area_removed(self, pos):
        self.area_edit_widget.hide()
        # remove the area that was clicked on
        for i, a in enumerate(self.selected_areas):
            if a.geometry().contains(pos):
                a.close()
                del self.selected_areas[i]

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
        self.selected_areas = []

    def save(self):
        '''Save the selected areas to a json file and quit the app'''
        outdict = {
            i: [a.geometry().x(), a.geometry().y(), a.geometry().width(), a.geometry().height()]
            for i, a in enumerate(self.selected_areas)
        }
        with open('rects.json', 'w') as outfile:
            json.dump(outdict, outfile)
        app.exit()


class AreaEditWidget(TransparentWidget):

    # add a signal that emits the area selected
    areaSelected = Signal(QRect)
    areaRemoved = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(opacity=0.25)
        # select area
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        # coords of mouse click
        self.origin = QPoint()

    def mousePressEvent(self, event):
        # left click starts the rubber band
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()
        # right click on a selected area to remove it
        if event.button() == Qt.RightButton:
            self.areaRemoved.emit(event.pos())

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberband.hide()
            area_selected = self.rubberband.geometry()
            self.areaSelected.emit(area_selected)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    widget = AreaSelectTool(size)
    widget.show()

    sys.exit(app.exec_())
