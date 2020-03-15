from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyautogui
import sys
import window_functions as wf
from config import regions_of_interest as roi

from CreepStacker import DoubleCreepStack


class HonMacroController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.hon_windows = wf.init_hon_windows()
        self.tasks = []
        self.initUI()
        self.threadpool = QThreadPool()

    def initUI(self):
        btn1 = QPushButton("stack easy legion creep", self)
        btn1.move(30, 50)

        btn2 = QPushButton("move top right", self)
        btn2.move(200, 50)

        btn3 = QPushButton("reset hon windows", self)
        btn3.move(30, 150)

        btn1.clicked.connect(self.stack_easy_legion_creep)
        btn2.clicked.connect(self.move_top_right)
        btn3.clicked.connect(self.re_initialize_hon_windows)

        self.statusBar()

        self.setGeometry(370, 300, 290, 300)
        self.setWindowTitle('Event sender')
        self.show()

    # need a task queue
    # each program loop, check conditions, and execute tasks if applicable
    def stack_easy_legion_creep(self):
        camp_location = roi.screen_size_1600x1024['legion_easy_double_pull']
        creepStacker = DoubleCreepStack(self.hon_windows[0], camp_location)
        self.threadpool.start(creepStacker)

    @pyqtSlot()
    def move_top_right(self):
        pyautogui.moveTo(2000, 200)
        self.tasks.append('move_top_right')

    @pyqtSlot()
    def re_initialize_hon_windows(self):
        self.hon_windows = wf.init_hon_windows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HonMacroController()
    sys.exit(app.exec_())