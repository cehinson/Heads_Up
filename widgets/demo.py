
import sys

from screen_select_widget import ScreenSelectWidget

from PySide2.QtWidgets import (
    QApplication,
    QPushButton
)


def select_area(caller):
    select_area_button.hide()
    print("select area clicked")
    ssw.show()


app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()

ssw = ScreenSelectWidget(size.width(), size.height())
select_area_button = QPushButton("Select Area")
select_area_button.clicked.connect(select_area)
select_area_button.show()
app.exec_()
sys.exit()
