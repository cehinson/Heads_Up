
import sys

from PySide2.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)

from PySide2.QtCore import (
    Qt
)


class TransparentWidget(QWidget):
    '''
    A semi-transparent widget
    '''

    def __init__(self, opacity=0.0, frameless=True):
        QWidget.__init__(self)
        # make the window transparent
        self.setWindowOpacity(opacity)
        # remove the top bar
        if frameless:
            self.setWindowFlag(Qt.FramelessWindowHint)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    widget = TransparentWidget()
    widget.resize(size.width(), size.height())
    widget.show()

    sys.exit(app.exec_())
