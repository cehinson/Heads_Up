import sys

from PySide2.QtWidgets import (QApplication, QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt


class HeadsUpWidget(QWidget):
    '''
    A semi-transparent window that:
        - always stays on top
        - sends mouse / keyboard events through
    '''

    def __init__(self, opacity=0.25):
        QWidget.__init__(self)
        # allow all events to pass through this window
        self.setWindowFlag(Qt.WindowTransparentForInput)
        # keep the window on top
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # make the window transparent
        self.setWindowOpacity(opacity)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    widget = HeadsUpWidget()
    widget.resize(size.width(), size.height())
    widget.show()

    sys.exit(app.exec_())
