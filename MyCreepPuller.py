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

# TODO: wildsoul
# TODO: game clock triggering
# TODO: team detection (hellbourne/legion)
# TODO: collect legion points

import pyautogui
import time
import window_functions
import BoundingBox as bb
from pynput import keyboard
from pynput.mouse import Button, Controller

mouse = Controller()


#globals
COMMAND_HOLD='h'
HOTKEY_WARBEAST='5'
HOTKEY_HOUND1='6'
HOTKEY_HOUND2='7'

hero_location = bb.Point(71, 951)
top_legion_pull_point1 = bb.Point(142, 847)
mid_dropoff_point = bb.Point(113, 948)

hb_fountain = bb.Point(219,843)

def issue_shift_click_seq(cmd_file,hon_window):
    cmd_list = open(cmd_file,'r').read().split('\n')
    
    pyautogui.keyDown('shift')
    time.sleep(.05)
    for cmd in cmd_list:
        cmd_xy =  cmd.split(',')
        cmd_pt = bb.Point(int(cmd_xy[0]),int(cmd_xy[1]))
        pyautogui.click(x=int(cmd_xy[0]),y=int(cmd_xy[1]),button='right')
#         hon_window.right_click(cmd_pt)

    pyautogui.keyUp('shift')
    time.sleep(.05)
    

def pull_creep_hb(hon_window):
    print('pulling hb...')
    
    #NOTE: warbeast should be outwardly facing at hb_fountain
    
    # Run to pull staging location (now that hounds are permanent, can this be in the fountain?)
    # BUG: SELECTION FROM KEYBOARD DOESN'T WORK CURRENTLY...
#     pyautogui.press(HOTKEY_HOUND1)
#     time.sleep(1)
    issue_shift_click_seq('config/wb_hb_bot.txt',hon_window)
    time.sleep(5.9)
#     pyautogui.press(HOTKEY_HOUND2)
#     time.sleep(.05)
    issue_shift_click_seq('config/wb_hb_top.txt',hon_window)
    return
    
if __name__=="__main__":
    hon_windows = window_functions.init_hon_windows()
    hon_window = hon_windows[0]

    hon_window.set_foreground()
    def on_activate_d():
        pull_creep_hb(hon_window)
    def on_activate_e():
        h.stop()

    with keyboard.GlobalHotKeys({
            '<ctrl>+d': on_activate_d,
            '<ctrl>+e': on_activate_e}) as h:
        h.join()
#     pull_creep_hb()
    

