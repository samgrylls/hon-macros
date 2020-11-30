# tentative location: X:   71 Y:  958
# for hero position

# f3 to select wolves
# double click X: 1391 Y:  930 for wolf 1
# 1431 Y:  920 for wolf 2

# X:  142 Y:  847 top pull if legion?
# then shift click
# takes 28s from 71, 958
# need to send them at :10 or :40

# then back to X:  113 Y:  948 to pull mid

# cadence needs to be: 10 pull, 40 pull, skip (spawn dogs at ~30), 40 pull, 10 pull, skip (spawn at 0), etc
# need to pop clarities in there too
# maybe need to get a wildsoul pull going too

# TODO: hellbourne side, wildsoul, use game clock triggering, etc

import pyautogui
import time
import window_functions
import BoundingBox as bb

hero_location = bb.Point(71, 951)
top_legion_pull_point1 = bb.Point(142, 847)
mid_dropoff_point = bb.Point(113, 948)

def pull_creep():
    select_wolf(1)
    pyautogui.keyDown('shift')
    hon_window.right_click(top_legion_pull_point1)
    time.sleep(0.1)
    hon_window.right_click(mid_dropoff_point)
    pyautogui.keyUp('shift')

    time.sleep(29)
    select_wolf(2)
    pyautogui.keyDown('shift')
    hon_window.right_click(top_legion_pull_point1)
    time.sleep(0.1)
    hon_window.right_click(mid_dropoff_point)
    pyautogui.keyUp('shift')

def move_to_spot():
    select_hero()
    hon_window.right_click(hero_location)

def select_wolf(num):
    pyautogui.hotkey(str(num))
    time.sleep(0.1)
    pyautogui.hotkey(str(num))

def check_arrival(point):
    hero_coords = hon_window.locate_hero(img_path='img/wb_minimap_icon.png')
    print(hero_coords.x, hero_coords.y)

    hon_window.screenshot(hero_coords, save_output=True)
    # print(hero_coords.as_dict())
    # print(self.creep_camp.location.x, self.creep_camp.location.y)
    return ((hero_coords.x < point.x)
            & (hero_coords.x + hero_coords.width > point.x)
            & (hero_coords.y < point.y)
            & (hero_coords.y + hero_coords.height > point.y))

def select_hero():
    pyautogui.hotkey('f1')


def spawn_and_group_wolves():
    pyautogui.hotkey()


def init_warbeast():
    # level up wolves
    # could also level up with a hotkey, idk
    hon_window.left_click(bb.Point(731, 884))
    time.sleep(0.1)
    pyautogui.hotkey('q')11
    time.sleep(0.5)
    # group them
    # select all non-hero units
    pyautogui.hotkey('f3')
    time.sleep(0.1)
    # wolf 1 portrait location
    hon_window.left_click(bb.Point(1393, 927))
    time.sleep(0.05)
    hon_window.left_click(bb.Point(1393, 927))
    # return
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', '1')
    time.sleep(0.1)

    pyautogui.hotkey('f3')
    time.sleep(0.1)
    # wolf 2
    hon_window.left_click(bb.Point(1439, 927))
    time.sleep(0.05)
    hon_window.left_click(bb.Point(1439, 927))
    pyautogui.hotkey('ctrl', '2')






if __name__=="__main__":
    hon_windows = window_functions.init_hon_windows()
    hon_window = hon_windows[0]

    hon_window.set_foreground()

    init_warbeast()

