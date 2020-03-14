from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
import pyautogui, sys
from PyQt5.QtCore import pyqtSlot

class HonMacroController(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn1 = QPushButton("move top left", self)
        btn1.move(30, 50)

        btn2 = QPushButton("move top right", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.move_top_left)
        btn2.clicked.connect(self.move_top_right)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    @pyqtSlot()
    def move_top_left(self):
        pyautogui.moveTo(100, 200)

    @pyqtSlot()
    def move_top_right(self):
        pyautogui.moveTo(2000, 200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())