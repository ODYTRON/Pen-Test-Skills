#!/usr/bin/env python

import subprocess

# alternative for 32bit python "%SystemRoot%\Sysnative\msg.exe * you have been hacked by Kurz Dick"
command = "msg * you have been hacked by Kurz Dick"
subprocess.Popen(command, shell=True)
