
import sys

from transparent_widget import TransparentWidget

from PySide2.QtWidgets import (
    QApplication,
)

from PySide2.QtCore import (
    Qt
)


# TODO change to subclass TransparentWidget

class HeadsUpWidget(TransparentWidget):
    '''
    A semi-transparent window that:
        - always stays on top
        - sends mouse / keyboard events through
    '''

    def __init__(self, opacity=0.25):
        super().__init__(opacity=opacity, frameless=True)
        # allow all events to pass through this window
        self.setWindowFlag(Qt.WindowTransparentForInput)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    widget = HeadsUpWidget()
    widget.resize(size.width(), size.height())
    widget.show()

    sys.exit(app.exec_())
