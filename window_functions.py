import pyautogui
import sys
import win32gui
import ctypes
from PIL import Image
import mss


class HonWindow:
    def __init__(self, rect):
        self.bounding_box = rect
        # get screenshotter
        self.sct = mss.mss()
        bb_dict_keys = ['left', 'top', 'width', 'height']
        self.bounding_box_dict = dict(zip(bb_dict_keys, self.bounding_box))

    def screenshot(self):

        screenshot = self.sct.grab(self.bounding_box_dict)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save('test.png')
        return img


# need simple xgb model to parse time
def init_hon_windows(handles):

    hon_windows = []
    handles = get_window_titles()
    for handle in handles:
        rect = win32gui.GetWindowRect(handle)
        hon_windows.append(HonWindow(rect))
    return hon_windows


def find_img_in_window(hon_window):
    img = Image.open('img/hon_clock.PNG')

    screenshot = hon_window.screenshot()
    img_location = pyautogui.locate(img, screenshot)
    # need to just get the overlay, not the actual game clock
    # that way it wont matter what the time is

    return img_location


def get_window_titles():

    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    handles = []

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            text = GetWindowText(hwnd, buff, length + 1)
            window_title = buff.value
            if window_title == 'Heroes of Newerth':
                handles.append(hwnd)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return handles


if __name__=='__main__':
    handles = get_window_titles()
    hon_windows = init_hon_windows(handles)
    clock_location = find_img_in_window(hon_windows[0])
    print(clock_location)
    print(hon_windows[0].bounding_box)