from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from datetime import datetime
from GameTimeChecker import GameTimeChecker, GameTimeClock
from window_functions import HonWindow
from LogListener import LogListener

import pyautogui
import sys
import window_functions as wf
from config import regions_of_interest as roi

from CreepStacker import DoubleCreepStack

HEROES = ['Wildsoul', 'War Beast', 'Ophelia']


class HonMacroController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.game_time_signal = pyqtSignal()
        # uic.loadUi('ui/base.ui', self)
        self.hon_windows = wf.init_hon_windows()

        if len(self.hon_windows) == 0:
            raise ValueError("No hon windows found")
        self.tasks = []

        self.window_frames = []
        self.threadpool = QThreadPool()
        self.clockThread = QThreadPool()
        self.initUI()
        self.show()
        self.is_clock_running = False

        print(self.findChild(QFrame, 'frame1'))

    # def init_window_frame(self, honWindowFrame):
    #     honWindowFrame.title = QLabel("No hero", self)
    #     honWindowFrame.title.move(honWindowFrame.xPosition, 10)
    #     honWindowFrame.push_button = QPushButton("Run task", self)
    #     honWindowFrame.push_button.move(honWindowFrame.xPosition, 50)
    #     honWindowFrame.action_dropdown = QComboBox(self)
    #     honWindowFrame.action_dropdown.move(honWindowFrame.xPosition, 100)
    #     honWindowFrame.condition_dropdown = QComboBox(self)
    #     honWindowFrame.condition_dropdown.move(honWindowFrame.xPosition, 150)

    @pyqtSlot()
    def choose_hero(self, text):
        idx = self.dropdowns.index(self.sender())
        self.labels[idx].setText(f"Window {idx} hero: {text}")
        self.hon_windows[idx].hero = text

    @pyqtSlot()
    def show_window(self):
        idx = self.buttons.index(self.sender())
        self.hon_windows[idx].set_foreground()

    def initUI(self):
        print(len(self.hon_windows))

        bottom_offset = 150
        self.buttons = []
        self.labels = []
        self.dropdowns = []
        for idx, val in enumerate(self.hon_windows):
            label = QLabel(self)
            label.setText(f"Window {idx}: {val.hero}")
            label.move(30, bottom_offset)
            label.show()
            self.labels.append(label)

            show_window_button = QPushButton("show", self)
            show_window_button.move(270, bottom_offset)
            show_window_button.clicked.connect(self.show_window)
            self.buttons.append(show_window_button)

            dropdown = QComboBox(self)
            dropdown.addItems(HEROES)
            dropdown.move(150, bottom_offset)
            dropdown.currentTextChanged.connect(lambda text: self.choose_hero(text))
            self.dropdowns.append(dropdown)
            
            bottom_offset += 50

        self.log_listener = LogListener()
        self.game_time = QLabel("Game time", self)
        self.game_time.setAlignment(Qt.AlignCenter)
        self.game_time.setText("123")
        self.game_time.show()


        btn1 = QPushButton("stack easy legion creep", self)
        btn1.move(30, 50)

        btn2 = QPushButton("start clock", self)
        btn2.move(150, 50)

        btn3 = QPushButton("reset hon windows", self)
        btn3.move(30, 100)

        btn4 = QPushButton("reset game time", self)
        btn4.move(150, 100)

        btn1.clicked.connect(lambda: self.stack_easy_legion_creep(self.hon_windows[0]))
        btn2.clicked.connect(self.start_clock)
        btn3.clicked.connect(self.re_initialize_hon_windows)
        btn4.clicked.connect(self.trigger_update_game_time)

        self.statusBar()

        self.setGeometry(370, 300, 490, 300)
        self.setWindowTitle('Event sender')
        self.show()

    # need a task queue
    # each program loop, check conditions, and execute tasks if applicable
    def stack_easy_legion_creep(self, hon_window):
        camp_location = roi.screen_size_1600x1024['legion_easy_double_stack']
        creepStacker = DoubleCreepStack(hon_window, camp_location)
        self.threadpool.start(creepStacker)

    @pyqtSlot()
    def trigger_update_game_time(self):
        game_time_checker = GameTimeChecker(self.log_listener, self.update_game_time, self.hon_windows[0])
        self.threadpool.start(game_time_checker)

    def update_game_time(self, game_time_result):
        self.game_time.setText(f"{game_time_result.val.format_time()}")

    @pyqtSlot()
    def start_clock(self):
        if not self.is_clock_running:
            game_time_clock = GameTimeClock(self.log_listener, self.update_game_time, self.set_clock_running, self.hon_windows[0])
            self.threadpool.start(game_time_clock)
        else:
            print('Clock already started')

    def set_clock_running(self):
        self.is_clock_running = True

    @pyqtSlot()
    def re_initialize_hon_windows(self):
        self.hon_windows = wf.init_hon_windows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HonMacroController()
    sys.exit(app.exec_())