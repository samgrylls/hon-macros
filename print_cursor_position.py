import pyautogui, sys
from pynput.mouse import Listener
import window_functions


hon_windows = window_functions.init_hon_windows()
hon_window = hon_windows[0]


def on_click(x, y, button, pressed):
    if pressed:
        print_cursor_position(window=hon_window)


def print_cursor_position(window=None):
    x, y = pyautogui.position()
    if window:
        x -= window.bounding_box.x
        y -= window.bounding_box.y
    positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    print(positionStr)


if __name__=='__main__':

    with Listener(on_click=on_click) as listener:
        listener.join()


# 841, 26
# 369, 943
