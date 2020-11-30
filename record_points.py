from pynput import keyboard
from pynput.mouse import Button, Controller



# Press ctrl+a to record a mouse position to log
# press ctrl+e to end log and point collection

mouse = Controller()

log_file = open('pos_log.txt','a+')
log_file.write('~~~~~~~~~\n')

def for_canonical(f):
    return lambda k: f(l.canonical(k))


def on_activate_a():
    x,y = mouse.position
    log_file.write(f'{x},{y}\n')
    print(f'{x},{y}')

def on_activate_e():
    h.stop()
    log_file.close()

with keyboard.GlobalHotKeys({
        '<ctrl>+a': on_activate_a,
        '<ctrl>+e': on_activate_e}) as h:
    h.join()