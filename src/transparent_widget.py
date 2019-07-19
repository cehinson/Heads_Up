
import sys

from PySide2.QtWidgets import (
    QApplication,
    QWidget,
)

from PySide2.QtCore import (
    Qt
)


class TransparentWidget(QWidget):
    ''' A semi-transparent widget '''

    def __init__(self, opacity=0.5, frameless=True):
        QWidget.__init__(self, parent=None)

        self.setWindowOpacity(opacity)

        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        # remove the top bar
        if frameless:
            self.setWindowFlag(Qt.FramelessWindowHint)

        # closing this window also deletes it
        self.setAttribute(Qt.WA_DeleteOnClose)


class HeadsUpWidget(TransparentWidget):
    '''
    A transparent widget that:
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

    widget = TransparentWidget()
    widget.resize(size.width(), size.height())
    widget.show()

    sys.exit(app.exec_())
