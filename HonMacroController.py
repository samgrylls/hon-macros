from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from window_functions import HonWindow
import pyautogui
import sys
import window_functions as wf
from config import regions_of_interest as roi

from CreepStacker import DoubleCreepStack


class HonWindowFrame(HonWindow):
    def __init__(self, xPosition):
        self.xPosition = xPosition
        self.title = None
        self.push_button = None
        self.action_dropdown = None
        self.condition_dropdown = None


class HonMacroController(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/base.ui', self)
        self.hon_windows = wf.init_hon_windows()

        if len(self.hon_windows) == 0:
            raise ValueError("No hon windows found")
        self.tasks = []

        self.window_frames = []
        self.threadpool = QThreadPool()


        # for idx, val in enumerate([20, 120, 220, 320]):
        #     self.window_frames.append(HonWindowFrame(val))
        #     self.init_window_frame(self.window_frames[idx])
        self.initUI()
        self.show()

        print(self.findChild(QFrame, 'frame1'))

    def init_window_frame(self, honWindowFrame):
        honWindowFrame.title = QLabel("No hero", self)
        honWindowFrame.title.move(honWindowFrame.xPosition, 10)
        honWindowFrame.push_button = QPushButton("Run task", self)
        honWindowFrame.push_button.move(honWindowFrame.xPosition, 50)
        honWindowFrame.action_dropdown = QComboBox(self)
        honWindowFrame.action_dropdown.move(honWindowFrame.xPosition, 100)
        honWindowFrame.condition_dropdown = QComboBox(self)
        honWindowFrame.condition_dropdown.move(honWindowFrame.xPosition, 150)

    def initUI(self):
        print(len(self.hon_windows))
        btn1 = QPushButton("stack easy legion creep", self)
        btn1.move(30, 50)

        btn2 = QPushButton("move top right", self)
        btn2.move(200, 50)

        btn3 = QPushButton("reset hon windows", self)
        btn3.move(30, 150)

        btn1.clicked.connect(lambda: self.stack_easy_legion_creep(self.hon_windows[0]))
        btn2.clicked.connect(self.move_top_right)
        btn3.clicked.connect(self.re_initialize_hon_windows)

        self.statusBar()

        self.setGeometry(370, 300, 290, 300)
        self.setWindowTitle('Event sender')
        self.show()

    # need a task queue
    # each program loop, check conditions, and execute tasks if applicable
    def stack_easy_legion_creep(self, hon_window):
        camp_location = roi.screen_size_1600x1024['legion_easy_double_stack']
        creepStacker = DoubleCreepStack(hon_window, camp_location)
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