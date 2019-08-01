
import sys

from PySide2.QtWidgets import (
    QApplication,
    QWidget,
)

from PySide2.QtCore import (
    Qt,
    QRect,
    QPoint,
)

from PySide2.QtGui import (
    QPainter,
    QBrush,
    QColor,
    QFont,
    QPen,
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


class BoundingBoxWidget(HeadsUpWidget):
    '''
    Identify objects that have been found on the screen
    '''

    def __init__(self, label="test"):
        # NOTE the parent widget only has 0.5 opacity so
        # we can still see the bounding box
        super().__init__(opacity=0.75)
        self.color = QColor('green')
        self.label = label
        # self.setGeometry(loc)
        # this makes the background entirely transparent
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, e):

        painter = QPainter(self)

        width = painter.device().width()
        height = painter.device().height()
        # size in pixels
        bbox_frame_size = 5

        brush = QBrush()
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)

        # top
        top_rect = QRect(0, 0, width, bbox_frame_size)
        painter.fillRect(top_rect, brush)
        # bottom
        bottom_rect = QRect(0, height-bbox_frame_size, width, bbox_frame_size)
        painter.fillRect(bottom_rect, brush)
        # left
        left_rect = QRect(0, 0, bbox_frame_size, height)
        painter.fillRect(left_rect, brush)
        # right
        right_rect = QRect(width-bbox_frame_size, 0, bbox_frame_size, height)
        painter.fillRect(right_rect, brush)

        # draw text
        loc = QPoint(painter.device().width() // 2, painter.device().height()-(bbox_frame_size+1))

        pen = QPen()
        pen.setColor(self.color)
        painter.setPen(pen)

        font = QFont()
        font.setPointSize(16)
        painter.setFont(font)

        painter.drawText(loc, self.label)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()

    widget = BoundingBoxWidget()
    widget.resize(size.width() // 2, size.height() // 2)
    widget.show()

    sys.exit(app.exec_())
