import pyautogui
import sys
import win32gui
import ctypes
from PIL import Image
import mss
import BoundingBox as bb
import time
from config import regions_of_interest as roi


class HonWindow:
    def __init__(self, coords, handle):
        self.bounding_box = bb.BoundingBox(coords, mode='corners')
        # get screenshotter
        self.handle = handle
        self.sct = mss.mss()
        minimap = roi.screen_size_1600x1024['minimap']
        self.minimap_bounding_box = bb.BoundingBox([self.bounding_box.x + minimap.x,
                                                   self.bounding_box.y + minimap.y,
                                                   minimap.width,
                                                   minimap.height], mode='relative')

        clock = roi.screen_size_1600x1024['in_game_clock']
        self.clock_bounding_box = bb.BoundingBox([self.bounding_box.x + clock.x,
                                                   self.bounding_box.y + clock.y,
                                                   clock.width,
                                                   clock.height], mode='relative')

    def set_foreground(self):
        win32gui.SetForegroundWindow(self.handle)

    def screenshot(self):
        screenshot = self.sct.grab(self.bounding_box.as_dict())
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save('test.png')
        return img

    def minimap_screenshot(self):
        screenshot = self.sct.grab(self.minimap_bounding_box.as_dict())
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save('minimap_test.png')
        return img

    def clock_screenshot(self):
        screenshot = self.sct.grab(self.clock_bounding_box.as_dict())
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save('clock_test.png')
        return img

    def quadrant_screenshot(self, quadrant):
            screenshot = self.sct.grab(self.bounding_box.quadrant(quadrant).as_dict())
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            img.save('quadrant_test.png')
            return img

    def right_click(self, point):
        self.set_foreground()
        x = point.x + self.bounding_box.x
        y = point.y + self.bounding_box.y
        pyautogui.rightClick(x, y)

    def locate_hero(self):
        """
        Finds hero on the minimap by image search.
        :return: bounding box of hero location in window-relative coordinates
        """
        hero_minimap_location = find_img_in_window(self.minimap_screenshot(), 'img/ws_minimap_icon_2.png')

        return bb.BoundingBox([hero_minimap_location.x + self.minimap_bounding_box.x - self.bounding_box.x,
                               hero_minimap_location.y + self.minimap_bounding_box.y - self.bounding_box.y,
                               hero_minimap_location.width,
                               hero_minimap_location.height], mode='relative')


# need simple xgb model to parse time
def init_hon_windows():

    hon_windows = []
    handles = get_window_handles(name='Heroes of Newerth')
    for handle in handles:
        rect = win32gui.GetWindowRect(handle)
        hon_windows.append(HonWindow(rect, handle))
    return hon_windows


def find_img_in_window(screenshot, img):
    img_location = pyautogui.locate(img, screenshot)
    if img_location is None:
        return bb.BoundingBox([-1, -1, 0, 0], mode='relative')
    # need to just get the overlay, not the actual game clock
    # that way it wont matter what the time is
    return bb.BoundingBox([img_location[0], img_location[1], img_location[2], img_location[3]], mode='relative')


def is_img_in_window(screenshot, img):
    return pyautogui.locate(img, screenshot)


def get_window_handles(name='Heroes of Newerth'):

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
            if window_title == name:
                handles.append(hwnd)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return handles


if __name__ == '__main__':
    handles = get_window_handles(name='Heroes of Newerth')
    hon_windows = init_hon_windows()
    time_img = Image.open('img/creep_pull_time.png')
    clock_location = find_img_in_window(hon_windows[0].clock_screenshot(), time_img)
    # print(clock_location)
    # print(clock_location)
    # print(hon_windows[0].bounding_box.as_dict())
    hon_windows[0].quadrant_screenshot('bottom_left')
    print(hon_windows[0].locate_hero().as_dict())
    # print(hon_windows[0].clock_screenshot().as_dict())