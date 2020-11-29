from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject, QCoreApplication, QThreadPool
import time
import sys
from LogListener import LogListener
from window_functions import HonWindow, init_hon_windows


class ResultObj(QObject):
    def __init__(self, val):
        self.val = val


class Signals(QObject):
    progress = pyqtSignal(object)


class GameTimeChecker(QRunnable):

    def __init__(self, log_listener, fn, hon_window: HonWindow, **kwargs):
        """
        :param hon_window: current HonWindow object
        :param creep_camps: list of CreepCamp objects
        """
        super().__init__()
        self.fn = fn
        self.hon_window = hon_window
        self.signals = Signals()
        self.kwargs = kwargs
        self.signals.progress.connect(fn)
        self.log_listener = log_listener

    @pyqtSlot()
    def run(self):
        self.hon_window.print_game_time_to_console()
        self.log_listener.check_for_logs()

        result = ResultObj(self.log_listener.check_game_time())
        self.signals.progress.emit(result)


class GameTimeClock(QRunnable):

    def __init__(self, log_listener, fn, hon_window: HonWindow):
        super().__init__()
        self.fn = fn
        self.signals = Signals()
        self.signals.progress.connect(fn)
        self.log_listener = log_listener
        self.hon_window = hon_window

    @pyqtSlot()
    def run(self):
        if self.log_listener.game_start_time is None:
            self.hon_window.print_game_time_to_console()
            self.log_listener.check_for_logs()
        while True:
            result = ResultObj(self.log_listener.check_game_time())
            self.signals.progress.emit(result)
            time.sleep(1)




if __name__=="__main__":

    w = init_hon_windows()

    app = QCoreApplication(sys.argv)
    hello = GameTimeChecker(execute_this_fn, w[0])
    hello.signals.finished.connect(check)

    QThreadPool.globalInstance().start(hello)
    sys.exit(app.exec_())

