import pyautogui
import sys
import win32gui
import ctypes
from PIL import Image
import PIL.ImageOps
import mss
import BoundingBox as bb
import time
from config import regions_of_interest as roi
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


class HonWindow:
    def __init__(self, coords, handle):
        self.bounding_box = bb.BoundingBox(coords, mode='corners')
        # get screenshotter
        self.handle = handle
        self.hero = None
        self.sct = mss.mss()
        self.minimap = roi.screen_size_1600x1024['minimap']
        self.clock = roi.screen_size_1600x1024['in_game_clock']

    def print_game_time_to_console(self, sleep_time=0.1):
        self.set_foreground()
        time.sleep(sleep_time)
        pyautogui.hotkey('ctrl', 'f8')
        time.sleep(sleep_time)
        pyautogui.write('printserverstatus')
        time.sleep(sleep_time)
        pyautogui.press('enter')
        time.sleep(sleep_time)
        pyautogui.write('flushlogs')
        time.sleep(sleep_time)
        pyautogui.press('enter')
        time.sleep(sleep_time)
        pyautogui.hotkey('ctrl', 'f8')


    def set_foreground(self):
        win32gui.SetForegroundWindow(self.handle)

    def screenshot(self, subregion=None, save_output=False):
        if subregion:
            screenshot = self.sct.grab(subregion.from_outside_box(self.bounding_box).as_dict())
        else:
            screenshot = self.sct.grab(self.bounding_box.as_dict())
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        if save_output:
            img.save('test1.png')
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

    def left_click(self, point):
        self.set_foreground()
        x = point.x + self.bounding_box.x
        y = point.y + self.bounding_box.y
        pyautogui.leftClick(x, y)

    def shift_right_click(self, point):
        self.set_foreground()
        x = point.x + self.bounding_box.x
        y = point.y + self.bounding_box.y
        pyautogui.keyDown('shift')
        time.sleep(0.01)
        pyautogui.rightClick(x, y)
        time.sleep(0.01)
        pyautogui.keyUp('shift')

    def locate_hero(self, img_path='img/ws_minimap_icon_2.png'):
        """
        Finds hero on the minimap by image search.
        :return: bounding box of hero location in window-relative coordinates
        """
        hero_minimap_location = find_img_in_window(self.screenshot(self.minimap), img_path)

        return bb.BoundingBox([hero_minimap_location.x + self.minimap.x,
                               hero_minimap_location.y + self.minimap.y,
                               hero_minimap_location.width,
                               hero_minimap_location.height], mode='relative')

    def get_hero_name(self):
        img = self.screenshot(subregion=roi.screen_size_1600x1024['hero_name'])
        img.save('test123.png')
        return pytesseract.image_to_string(img, config='--psm 13')

    def clock_image(self):
        return self.screenshot(self.clock)


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
    print(img_location)
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
    hero_name_image = Image.open('img/hero_name_sample.png')
    hero_name_location = find_img_in_window(hon_windows[0].screenshot(), hero_name_image)
    print(hero_name_location.as_dict())
    test = hon_windows[0].screenshot(subregion=roi.screen_size_1600x1024['hero_name'], save_output=True)

    print(hon_windows[0].get_hero_name())

