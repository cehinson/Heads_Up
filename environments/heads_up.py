import json
import pyautogui
from PySide2.QtWidgets import QApplication
import sys
# FIXME this seems like a hack...
sys.path.append('/Users/charles/projects/personal/heads-up/')
sys.path.append('/Users/charles/projects/personal/heads-up/widgets/')
from widgets import heads_up_widget

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True


def run():
    app = QApplication(sys.argv)

    with open('/Users/charles/projects/personal/heads-up/environments/rects.json', 'r') as f:
        rects = json.load(f)

    widgets = []
    for rect in rects.values():
        print(rect)
        widget = heads_up_widget.HeadsUpWidget()
        widget.setStyleSheet('background-color: rgb(255, 0, 0)')
        widget.setGeometry(*rect)
        widget.show()
        widgets.append(widget)

    sys.exit(app.exec_())

    while True:
        pass


if __name__ == '__main__':
    run()
